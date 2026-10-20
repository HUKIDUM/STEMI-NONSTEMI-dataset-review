"""Download the small metadata/header samples listed in PLAN.md §3 (step S1).

Rules this module follows:
- Only files named by the hard-coded MANIFEST below, or derived from it by a
  fixed rule (seeded sample, RECORDS list), are fetched. Every derived path must
  match the source's allowed pattern, so waveforms (.dat/.mat/.h5) are refused.
- At most 500 MB per dataset folder, checked before and during each download.
- Files go to ``data/samples/<local_dir>/``. Existing files are never
  overwritten or deleted; they are logged as ``skipped_exists``.
- Every attempt is appended to ``results/download_manifest.csv`` with sha256 and,
  where the publisher gives one, the checksum match.
- Each run needs ``--approval`` text that records the user's OK (via team-lead).

Run from the project root (``-I`` because it reads downloaded files):
    .venv/bin/python -I src/stemi/review/fetch_samples.py ptb_xl --dry-run
    .venv/bin/python -I src/stemi/review/fetch_samples.py ptb_xl --approval "user OK 2026-10-20 via team-lead"
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
import csv
import hashlib
import http.client
import re
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SAMPLES_ROOT = PROJECT_ROOT / "data" / "samples"
MANIFEST_CSV = PROJECT_ROOT / "results" / "download_manifest.csv"

MAX_BYTES_PER_DATASET = 500 * 1024 * 1024       # PLAN §0 / team-lead brief
SAMPLE_SEED = 20261020                          # PLAN §3
USER_AGENT = "stemi-dataset-review/0.1 (metadata-only research sample; polite rate)"
REQUEST_DELAY_S = 0.25                          # per worker, between requests
TIMEOUT_S = 120
RETRIES = 4

MANIFEST_COLUMNS = [
    "dataset_id", "url", "local_path", "bytes", "sha256", "download_utc",
    "status", "checksum_source", "expected_checksum", "checksum_match", "approval",
]

PHYSIONET = "https://physionet.org/files/"
CHALLENGE = PHYSIONET + "challenge-2021/1.0.3/"
HEA = r"[A-Za-z0-9_\-/]+\.hea"


# --------------------------------------------------------------------------- manifest


@dataclass(frozen=True)
class Stage:
    """Files derived from already-downloaded files. ``rule(local_dir) -> relpaths``."""
    description: str
    rule: Callable[[Path], list[str]]
    pattern: str                      # every derived relpath must fully match this


@dataclass(frozen=True)
class Source:
    dataset_id: str
    base_url: str
    local_dir: str
    files: tuple[str, ...] = ()                       # fixed relpaths under base_url
    stages: tuple[Stage, ...] = ()
    sha256sums_url: str | None = None                 # streamed; only needed lines kept
    expected_md5: dict[str, str] = field(default_factory=dict)   # relpath -> md5 (cited)
    md5_source: str | None = None
    remote_names: dict[str, str] = field(default_factory=dict)   # relpath -> remote path


def _read_lines(path: Path) -> list[str]:
    return [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]


def seeded_sample(csv_path: Path, column: str, n: int, seed: int = SAMPLE_SEED) -> list[str]:
    """``n`` values of ``column`` drawn with a fixed seed from the whole table."""
    values = pd.read_csv(csv_path, usecols=[column])[column].dropna().astype(str)
    values = values.sort_values(kind="stable").reset_index(drop=True)
    return values.sample(n=min(n, len(values)), random_state=seed).sort_values().tolist()


def records_headers(records_file: str, prefix: str = "") -> Callable[[Path], list[str]]:
    """Every record in a WFDB RECORDS file -> ``<prefix><record>.hea``."""
    def rule(local: Path) -> list[str]:
        return [f"{prefix}{r}.hea" for r in _read_lines(local / records_file)]
    return rule


def challenge_group_records(folder: str) -> Callable[[Path], list[str]]:
    """Root Challenge RECORDS lists group folders; keep the ones under ``folder``."""
    def rule(local: Path) -> list[str]:
        groups = [g.rstrip("/") for g in _read_lines(local / "RECORDS")
                  if g.startswith(f"training/{folder}/")]
        return [f"{g}/RECORDS" for g in groups]
    return rule


def challenge_group_headers(folder: str) -> Callable[[Path], list[str]]:
    def rule(local: Path) -> list[str]:
        out = []
        for rec_file in sorted((local / "training" / folder).glob("g*/RECORDS")):
            group = rec_file.parent.relative_to(local).as_posix()
            out += [f"{group}/{r}.hea" for r in _read_lines(rec_file)]
        return out
    return rule


def _challenge(dataset_id: str, folder: str, local_dir: str | None = None) -> Source:
    return Source(
        dataset_id=dataset_id, base_url=CHALLENGE, local_dir=local_dir or dataset_id,
        files=("RECORDS",),
        stages=(
            Stage(f"g*/RECORDS of training/{folder}", challenge_group_records(folder),
                  rf"training/{re.escape(folder)}/g\d+/RECORDS"),
            Stage(f"every .hea listed in training/{folder}/g*/RECORDS",
                  challenge_group_headers(folder),
                  rf"training/{re.escape(folder)}/g\d+/[A-Za-z0-9_\-]+\.hea"),
        ),
        sha256sums_url=CHALLENGE + "SHA256SUMS.txt",
    )


# Publisher checksums, filled from the cited API record before download (empty = none)
# (read 2026-10-20; figshare computed_md5 == supplied_md5 for all three, zenodo "checksum")
SPH_MD5: dict[str, str] = {"metadata.csv": "8ef8e8789059a585c89c5302c7891909",
                           "code.csv": "9fafec6cc6e1ef8117e2964116654d05",
                           "rule.pdf": "8e84772f206d50f0e661c787cd4c905a"}
SPH_MD5_SOURCE = ("https://api.figshare.com/v2/articles/17912441 (metadata.csv), "
                  "/17912507 (code.csv), /19738468 (rule.pdf): computed_md5")
CODE15_MD5: dict[str, str] = {"exams.csv": "0107516d3f63864498fb77d15799cc95"}
CODE15_MD5_SOURCE = "https://zenodo.org/api/records/4916206 files[key=exams.csv].checksum"
DX_MAPS_BASE = "https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/"


def _build_manifest() -> dict[str, Source]:
    sources = [
        Source(
            "ptb_xl", PHYSIONET + "ptb-xl/1.0.3/", "ptb_xl",
            files=("ptbxl_database.csv", "scp_statements.csv"),
            stages=(Stage(f"20 records500 .hea, seed {SAMPLE_SEED} over ptbxl_database.csv:filename_hr",
                          lambda d: [f"{p}.hea" for p in
                                     seeded_sample(d / "ptbxl_database.csv", "filename_hr", 20)],
                          r"records500/\d{5}/\d{5}_hr\.hea"),),
            sha256sums_url=PHYSIONET + "ptb-xl/1.0.3/SHA256SUMS.txt",
        ),
        Source(
            "mimic_iv_ecg", PHYSIONET + "mimic-iv-ecg/1.0/", "mimic_iv_ecg",
            files=("record_list.csv", "machine_measurements.csv",
                   "machine_measurements_data_dictionary.csv", "waveform_note_links.csv"),
            stages=(Stage(f"50 .hea, seed {SAMPLE_SEED} over record_list.csv:path",
                          lambda d: [f"{p}.hea" for p in
                                     seeded_sample(d / "record_list.csv", "path", 50)],
                          r"files/p\d{4}/p\d+/s\d+/\d+\.hea"),),
            sha256sums_url=PHYSIONET + "mimic-iv-ecg/1.0/SHA256SUMS.txt",
        ),
        Source(
            "ptb_diagnostic", PHYSIONET + "ptbdb/1.0.0/", "ptb_diagnostic",
            files=("RECORDS", "CONTROLS", "README"),
            stages=(Stage("every .hea listed in RECORDS", records_headers("RECORDS"),
                          r"patient\d{3}/s\d{4}[_a-z]re\.hea"),),
            sha256sums_url=PHYSIONET + "ptbdb/1.0.0/SHA256SUMS.txt",
        ),
        Source(
            "incart", PHYSIONET + "incartdb/1.0.0/", "incart",
            files=("RECORDS", "README", "record-descriptions.txt",
                   "files-patients-diagnoses.txt", "ANNOTATORS"),
            stages=(Stage("every .hea listed in RECORDS", records_headers("RECORDS"),
                          r"I\d{2}\.hea"),),
            sha256sums_url=PHYSIONET + "incartdb/1.0.0/SHA256SUMS.txt",
        ),
        _challenge("cpsc_2018", "cpsc_2018"),
        _challenge("cpsc_extra", "cpsc_2018_extra"),
        _challenge("georgia", "georgia"),
        _challenge("ningbo", "ningbo"),
        _challenge("chapman_shaoxing", "chapman_shaoxing"),
        # U4: Challenge copies, kept inside the native dataset's folder (and its 500 MB cap)
        _challenge("ptb_xl_challenge", "ptb-xl", local_dir="ptb_xl/challenge-2021"),
        _challenge("ptb_diagnostic_challenge", "ptb", local_dir="ptb_diagnostic/challenge-2021"),
        Source(
            "sph", "https://ndownloader.figshare.com/files/", "sph",
            files=("metadata.csv", "code.csv", "rule.pdf"),
            remote_names={"metadata.csv": "34793152", "code.csv": "32630954",
                          "rule.pdf": "35284594"},
            expected_md5=SPH_MD5, md5_source=SPH_MD5_SOURCE,
        ),
        Source(
            "code15", "https://zenodo.org/records/4916206/files/", "code15",
            files=("exams.csv",),
            expected_md5=CODE15_MD5, md5_source=CODE15_MD5_SOURCE,
        ),
        Source(   # U2: raw file over HTTPS only (no git, account or API)
            "dx_maps", DX_MAPS_BASE, "challenge_label_maps",
            files=("dx_mapping_scored.csv", "dx_mapping_unscored.csv"),
        ),
        Source(
            "snomed_names", PHYSIONET + "ecg-arrhythmia/1.0.0/", "challenge_label_maps",
            files=("ConditionNames_SNOMED-CT.csv",),
            sha256sums_url=PHYSIONET + "ecg-arrhythmia/1.0.0/SHA256SUMS.txt",
        ),
    ]
    return {s.dataset_id: s for s in sources}


MANIFEST: dict[str, Source] = _build_manifest()


# --------------------------------------------------------------------------- guards


class RefusedError(ValueError):
    pass


def check_allowed(source: Source, relpath: str, stage: Stage | None) -> None:
    """Refuse anything the manifest does not name (fixed file or stage pattern)."""
    if ".." in relpath.split("/") or relpath.startswith("/"):
        raise RefusedError(f"unsafe path: {relpath}")
    if stage is None:
        if relpath not in source.files:
            raise RefusedError(f"{relpath} is not a fixed file of {source.dataset_id}")
    elif not re.fullmatch(stage.pattern, relpath):
        raise RefusedError(f"{relpath} does not match {stage.pattern} ({source.dataset_id})")


def folder_bytes(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) if path.exists() else 0


class Budget:
    """Thread-safe byte budget for one dataset folder (500 MB)."""

    def __init__(self, used: int, limit: int = MAX_BYTES_PER_DATASET):
        self.used, self.limit = used, limit
        self._lock = threading.Lock()

    def take(self, n: int) -> None:
        with self._lock:
            if self.used + n > self.limit:
                raise RefusedError(f"500 MB cap: {self.used + n} bytes > {self.limit}")
            self.used += n


# --------------------------------------------------------------------------- http


def _request(url: str, method: str = "GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=TIMEOUT_S)


def _with_retries(fn):
    for attempt in range(RETRIES):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise RefusedError(f"HTTP {e.code}: login/credential wall, stopping") from e
            if e.code == 404 or attempt == RETRIES - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException):
            if attempt == RETRIES - 1:
                raise
        time.sleep(2 ** attempt * 2)


def head_size(url: str) -> int | None:
    def go():
        with _request(url, "HEAD") as r:
            n = r.headers.get("Content-Length")
            return int(n) if n else None
    return _with_retries(go)


class IncompleteDownload(ConnectionError):
    pass


def download(url: str, dest: Path, budget: Budget) -> tuple[int, str]:
    """Stream ``url`` to ``dest`` (never overwriting); returns (bytes, sha256).

    A failed attempt removes only the ``.part`` file that this attempt created,
    then retries. Bytes are charged to the budget once, not once per attempt.
    """
    if dest.exists():
        raise FileExistsError(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    if part.exists():                     # left by someone else: never touch it
        raise FileExistsError(part)
    charged = 0

    def charge_up_to(n: int) -> None:
        nonlocal charged
        if n > charged:
            budget.take(n - charged)
            charged = n

    def go():
        h, n = hashlib.sha256(), 0
        out = open(part, "xb")            # created by this attempt
        try:
            with _request(url) as r, out:
                declared = r.headers.get("Content-Length")
                if declared:
                    charge_up_to(int(declared))
                for chunk in iter(lambda: r.read(1 << 16), b""):
                    n += len(chunk)
                    charge_up_to(n)
                    h.update(chunk)
                    out.write(chunk)
                if declared and n != int(declared):
                    raise IncompleteDownload(f"{url}: {n} of {declared} bytes")
        except BaseException:
            out.close()
            part.unlink()
            raise
        return n, h.hexdigest()

    n, digest = _with_retries(go)
    part.rename(dest)                     # dest was checked absent above
    return n, digest


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sha256sums(lines, wanted: set[str]) -> dict[str, str]:
    """Pick ``<sha256>  <relpath>`` lines for ``wanted`` relpaths."""
    out = {}
    for ln in lines:
        parts = ln.strip().split(maxsplit=1)
        if len(parts) == 2 and parts[1].lstrip("*") in wanted:
            out[parts[1].lstrip("*")] = parts[0].lower()
    return out


def stream_sha256sums(url: str, wanted: set[str]) -> dict[str, str]:
    """Read SHA256SUMS.txt line by line; keep only the wanted lines (nothing saved)."""
    def go():
        with _request(url) as r:
            return parse_sha256sums((b.decode("utf-8", "replace") for b in r), wanted)
    return _with_retries(go)


# --------------------------------------------------------------------------- manifest log


_log_lock = threading.Lock()


def append_log(row: dict, path: Path = MANIFEST_CSV) -> None:
    with _log_lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        new = not path.exists()
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
            if new:
                w.writeheader()
            w.writerow({k: row.get(k, "") for k in MANIFEST_COLUMNS})


# --------------------------------------------------------------------------- run


def _url(source: Source, relpath: str) -> str:
    return source.base_url + source.remote_names.get(relpath, relpath)


def fetch_files(source: Source, relpaths: list[str], stage: Stage | None, *, budget: Budget,
                approval: str, workers: int, log_path: Path = MANIFEST_CSV,
                samples_root: Path = SAMPLES_ROOT) -> list[dict]:
    for rp in relpaths:                                   # refuse before any request
        check_allowed(source, rp, stage)
    local = samples_root / source.local_dir

    def one(rp: str) -> dict:
        dest = local / rp
        row = {"dataset_id": source.dataset_id, "url": _url(source, rp),
               "local_path": dest.relative_to(PROJECT_ROOT).as_posix()
               if dest.is_relative_to(PROJECT_ROOT) else dest.as_posix(),
               "download_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "approval": approval}
        if dest.exists():
            row.update(status="skipped_exists", bytes=dest.stat().st_size, sha256=sha256_of(dest))
        else:
            try:
                n, digest = download(row["url"], dest, budget)
                row.update(status="downloaded", bytes=n, sha256=digest)
            except urllib.error.HTTPError as e:
                row.update(status=f"http_{e.code}")
            time.sleep(REQUEST_DELAY_S)
        row["_relpath"] = rp
        return row

    rows, error = [], None
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        for fut in [pool.submit(one, rp) for rp in relpaths]:
            try:
                rows.append(fut.result())
            except Exception as e:            # keep completed rows for the log
                error = error or e
    return rows, error


def attach_checksums(source: Source, rows: list[dict]) -> None:
    """Fill checksum_* columns from SHA256SUMS (streamed) or cited md5 values."""
    have = [r for r in rows if r.get("sha256")]
    if source.sha256sums_url and have:
        remote = {source.remote_names.get(r["_relpath"], r["_relpath"]) for r in have}
        sums = stream_sha256sums(source.sha256sums_url, remote)
        for r in have:
            exp = sums.get(source.remote_names.get(r["_relpath"], r["_relpath"]))
            r.update(checksum_source=source.sha256sums_url, expected_checksum=exp or "",
                     checksum_match=("not available" if exp is None
                                     else "yes" if exp == r["sha256"] else "no"))
    for r in have:
        md5 = source.expected_md5.get(r["_relpath"])
        if md5:
            local = PROJECT_ROOT / r["local_path"]
            got = hashlib.md5(local.read_bytes()).hexdigest()
            r.update(checksum_source=source.md5_source, expected_checksum=f"md5:{md5}",
                     checksum_match="yes" if got == md5 else "no")
        r.setdefault("checksum_match", "not available")


def run(dataset_id: str, *, approval: str, workers: int = 4, dry_run: bool = False) -> list[dict]:
    if dataset_id not in MANIFEST:
        raise RefusedError(f"{dataset_id} is not in the manifest: {sorted(MANIFEST)}")
    source = MANIFEST[dataset_id]
    local = SAMPLES_ROOT / source.local_dir
    cap_root = SAMPLES_ROOT / source.local_dir.split("/")[0]       # cap per dataset folder
    if dry_run:
        print(f"{dataset_id}: base {source.base_url} -> {local}")
        total = 0
        for rp in source.files:
            n = head_size(_url(source, rp))
            total += n or 0
            print(f"  {rp}: {n} bytes")
            time.sleep(REQUEST_DELAY_S)
        for st in source.stages:
            print(f"  then: {st.description} (pattern {st.pattern})")
        print(f"  fixed files total: {total} bytes; folder now {folder_bytes(cap_root)} bytes")
        return []
    if not approval.strip():
        raise RefusedError("--approval is required (user OK via team-lead)")
    budget = Budget(folder_bytes(cap_root))
    all_rows = []
    batches = [(list(source.files), None)] + [(None, st) for st in source.stages]
    for relpaths, stage in batches:
        if stage is not None:
            relpaths = stage.rule(local)
            print(f"{dataset_id}: {stage.description}: {len(relpaths)} files")
        rows, error = fetch_files(source, relpaths, stage, budget=budget, approval=approval,
                                  workers=workers)
        try:
            attach_checksums(source, rows)
        finally:
            for r in rows:                    # log what completed, even on failure
                append_log(r)
        all_rows += rows
        if error is not None:
            raise error
    counts = pd.Series([r["status"] for r in all_rows]).value_counts().to_dict()
    print(f"{dataset_id}: {counts}; folder {folder_bytes(cap_root)} bytes; "
          f"checksum {pd.Series([r['checksum_match'] for r in all_rows]).value_counts().to_dict()}")
    return all_rows


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset_id", choices=sorted(MANIFEST))
    ap.add_argument("--approval", default="", help="record of the user's OK (who/when)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true", help="HEAD sizes of fixed files only")
    args = ap.parse_args(argv)
    run(args.dataset_id, approval=args.approval, workers=args.workers, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

import csv
import functools
import hashlib
import http.server
import threading

import pandas as pd
import pytest

from stemi.review import fetch_samples as fs


@pytest.fixture
def server(tmp_path):
    """Local HTTP server over a temp 'remote' folder (no network)."""
    remote = tmp_path / "remote"
    remote.mkdir()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(remote))
    handler.log_message = lambda *a: None
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield remote, f"http://127.0.0.1:{httpd.server_address[1]}/"
    httpd.shutdown()


@pytest.fixture(autouse=True)
def no_delay(monkeypatch):
    monkeypatch.setattr(fs, "REQUEST_DELAY_S", 0)


def _source(base, **kw):
    stage = fs.Stage("headers from RECORDS", fs.records_headers("RECORDS"), r"r\d+\.hea")
    return fs.Source("toy", base, "toy", files=("RECORDS",), stages=(stage,), **kw)


def _fetch(src, rels, stage, tmp_path, limit=fs.MAX_BYTES_PER_DATASET):
    rows, error = fs.fetch_files(src, rels, stage, budget=fs.Budget(0, limit), approval="test",
                                 workers=2, log_path=tmp_path / "m.csv",
                                 samples_root=tmp_path / "samples")
    if error is not None:
        raise error
    return rows


def test_downloads_and_hashes(server, tmp_path):
    remote, base = server
    (remote / "RECORDS").write_text("r1\nr2\n")
    src = _source(base)
    rows = _fetch(src, ["RECORDS"], None, tmp_path)
    assert rows[0]["status"] == "downloaded"
    assert rows[0]["sha256"] == hashlib.sha256(b"r1\nr2\n").hexdigest()
    local = tmp_path / "samples" / "toy"
    assert src.stages[0].rule(local) == ["r1.hea", "r2.hea"]


def test_refuses_files_not_in_manifest(server, tmp_path):
    _, base = server
    src = _source(base)
    with pytest.raises(fs.RefusedError):
        _fetch(src, ["other.csv"], None, tmp_path)
    for bad in ["r1.dat", "r1.mat", "../r1.hea", "sub/r1.hea"]:   # waveforms, traversal
        with pytest.raises(fs.RefusedError):
            _fetch(src, [bad], src.stages[0], tmp_path)


def test_never_overwrites(server, tmp_path):
    remote, base = server
    (remote / "RECORDS").write_text("remote\n")
    dest = tmp_path / "samples" / "toy" / "RECORDS"
    dest.parent.mkdir(parents=True)
    dest.write_text("local\n")
    rows = _fetch(_source(base), ["RECORDS"], None, tmp_path)
    assert rows[0]["status"] == "skipped_exists"
    assert dest.read_text() == "local\n"


def test_500mb_cap_refuses(server, tmp_path):
    remote, base = server
    (remote / "RECORDS").write_text("x" * 100)
    with pytest.raises(fs.RefusedError, match="cap"):
        _fetch(_source(base), ["RECORDS"], None, tmp_path, limit=50)
    assert not (tmp_path / "samples" / "toy" / "RECORDS").exists()
    assert not (tmp_path / "samples" / "toy" / "RECORDS.part").exists()


def test_missing_file_logged_not_raised(server, tmp_path):
    _, base = server
    rows = _fetch(_source(base), ["RECORDS"], None, tmp_path)
    assert rows[0]["status"] == "http_404"


def test_parse_sha256sums_keeps_wanted_only():
    lines = ["aa  RECORDS\n", "bb  r1.hea\n", "cc  r1.dat\n"]
    assert fs.parse_sha256sums(lines, {"RECORDS", "r1.hea"}) == {"RECORDS": "aa", "r1.hea": "bb"}


def test_checksum_match_from_sha256sums(server, tmp_path, monkeypatch):
    remote, base = server
    (remote / "RECORDS").write_text("r1\n")
    good = hashlib.sha256(b"r1\n").hexdigest()
    (remote / "SHA256SUMS.txt").write_text(f"{good}  RECORDS\n")
    src = _source(base, sha256sums_url=base + "SHA256SUMS.txt")
    rows = _fetch(src, ["RECORDS"], None, tmp_path)
    fs.attach_checksums(src, rows)
    assert rows[0]["checksum_match"] == "yes"


def test_seeded_sample_is_deterministic(tmp_path):
    p = tmp_path / "t.csv"
    pd.DataFrame({"path": [f"x{i}" for i in range(100)]}).to_csv(p, index=False)
    a = fs.seeded_sample(p, "path", 5)
    assert a == fs.seeded_sample(p, "path", 5) and len(set(a)) == 5


def test_challenge_rules(tmp_path):
    (tmp_path / "RECORDS").write_text("training/georgia/g1/\ntraining/georgia/g2/\n"
                                      "training/ningbo/g1/\n")
    assert fs.challenge_group_records("georgia")(tmp_path) == [
        "training/georgia/g1/RECORDS", "training/georgia/g2/RECORDS"]
    g1 = tmp_path / "training" / "georgia" / "g1"
    g1.mkdir(parents=True)
    (g1 / "RECORDS").write_text("E00001\nE00002\n")
    src = fs.MANIFEST["georgia"]
    hdrs = fs.challenge_group_headers("georgia")(tmp_path)
    assert hdrs == ["training/georgia/g1/E00001.hea", "training/georgia/g1/E00002.hea"]
    for h in hdrs:
        fs.check_allowed(src, h, src.stages[1])
    with pytest.raises(fs.RefusedError):
        fs.check_allowed(src, "training/georgia/g1/E00001.mat", src.stages[1])


def test_manifest_patterns_reject_waveforms():
    cases = {"ptb_xl": "records500/00000/00001_hr.dat",
             "mimic_iv_ecg": "files/p1000/p10000032/s40689238/40689238.dat",
             "ptb_diagnostic": "patient001/s0010_re.dat", "incart": "I01.atr"}
    for ds, bad in cases.items():
        src = fs.MANIFEST[ds]
        with pytest.raises(fs.RefusedError):
            fs.check_allowed(src, bad, src.stages[0])
        fs.check_allowed(src, bad.rsplit(".", 1)[0] + ".hea", src.stages[0])


def test_append_log_never_rewrites(tmp_path):
    p = tmp_path / "m.csv"
    fs.append_log({"dataset_id": "a"}, p)
    fs.append_log({"dataset_id": "b"}, p)
    rows = list(csv.DictReader(open(p)))
    assert [r["dataset_id"] for r in rows] == ["a", "b"]
    assert list(rows[0]) == fs.MANIFEST_COLUMNS


def test_run_requires_approval():
    with pytest.raises(fs.RefusedError, match="approval"):
        fs.run("ptb_xl", approval=" ")
    with pytest.raises(fs.RefusedError):
        fs.run("not_a_dataset", approval="x")


def test_retry_after_dropped_connection(tmp_path, monkeypatch):
    """First GET sends half the body then closes; the retry must succeed (2026-10-20 bug)."""
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    body = b"x" * 5000
    calls = {"n": 0}

    class Flaky(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            calls["n"] += 1
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body if calls["n"] > 1 else body[:2000])
            self.close_connection = True

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Flaky)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        budget = fs.Budget(0, 6000)                       # would fail if charged twice
        dest = tmp_path / "f.csv"
        n, digest = fs.download(f"http://127.0.0.1:{httpd.server_address[1]}/f.csv", dest, budget)
    finally:
        httpd.shutdown()
    assert calls["n"] == 2 and n == 5000 and dest.read_bytes() == body
    assert budget.used == 5000
    assert not (tmp_path / "f.csv.part").exists()


def test_foreign_part_file_left_alone(server, tmp_path):
    remote, base = server
    (remote / "RECORDS").write_text("r1\n")
    part = tmp_path / "samples" / "toy" / "RECORDS.part"
    part.parent.mkdir(parents=True)
    part.write_text("someone else's")
    with pytest.raises(FileExistsError):
        _fetch(_source(base), ["RECORDS"], None, tmp_path)
    assert part.read_text() == "someone else's"


def test_only_must_name_fixed_files():
    with pytest.raises(fs.RefusedError):
        fs.run("mimic_iv_ecg", approval="x", only=["files/p1000/x.dat"])


def test_skip_sha256sums_marks_not_available(server, tmp_path):
    remote, base = server
    (remote / "RECORDS").write_text("r1\n")
    src = _source(base, sha256sums_url=base + "missing.txt")      # would 404 if streamed
    rows = _fetch(src, ["RECORDS"], None, tmp_path)
    fs.attach_checksums(src, rows, skip_sha256sums=True)
    assert rows[0]["checksum_match"] == "not available"
    assert "skipped" in rows[0]["checksum_source"]


def test_filter_groups():
    paths = ["training/georgia/g1/RECORDS", "training/georgia/g10/RECORDS",
             "training/georgia/g1/E00001.hea", "training/georgia/g2/E01001.hea"]
    assert fs.filter_groups(paths, ["g1"]) == [paths[0], paths[2]]
    assert fs.filter_groups(paths, None) == paths


class _RangeServer:
    """Serves one body; honours Range with 206. Request 1 is cut off after `cut` bytes."""

    def __init__(self, body, cut=None, bad_range=False, ignore_range=False):
        self.body, self.cut, self.calls, self.ranges = body, cut, 0, []
        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_HEAD(self):
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()

            def do_GET(self):
                outer.calls += 1
                rng = self.headers.get("Range")
                outer.ranges.append(rng)
                start = int(rng.split("=")[1].rstrip("-")) if rng else 0
                if rng and not ignore_range:
                    self.send_response(206)
                    first = start + 1 if bad_range else start
                    self.send_header("Content-Range", f"bytes {first}-{len(body)-1}/{len(body)}")
                    data = body[start:]
                else:
                    self.send_response(200)
                    data = body
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                if outer.calls == 1 and cut is not None:
                    self.wfile.write(data[:cut])
                else:
                    self.wfile.write(data)
                self.close_connection = True

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}/f.csv"


def test_dropped_connection_resumes_with_range(tmp_path, monkeypatch):
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    body = bytes(range(256)) * 40
    srv = _RangeServer(body, cut=3000)
    try:
        budget = fs.Budget(0, len(body))                # fails if charged twice
        n, digest = fs.download(srv.url, tmp_path / "f.csv", budget)
    finally:
        srv.httpd.shutdown()
    assert srv.ranges == [None, "bytes=3000-"]
    assert (tmp_path / "f.csv").read_bytes() == body and n == len(body)
    assert digest == hashlib.sha256(body).hexdigest()


def test_resume_existing_part_only_with_flag(tmp_path, monkeypatch):
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    body = b"abcdefghij" * 100
    srv = _RangeServer(body)
    part = tmp_path / "f.csv.part"
    part.write_bytes(body[:400])
    try:
        with pytest.raises(FileExistsError):
            fs.download(srv.url, tmp_path / "f.csv", fs.Budget(0))
        budget = fs.Budget(400, len(body))               # part already counted by folder_bytes
        fs.download(srv.url, tmp_path / "f.csv", budget, resume=True)
    finally:
        srv.httpd.shutdown()
    assert srv.ranges == ["bytes=400-"]
    assert (tmp_path / "f.csv").read_bytes() == body and not part.exists()


def test_resume_200_restarts_cleanly(tmp_path, monkeypatch):
    body = b"0123456789" * 50
    srv = _RangeServer(body, ignore_range=True)
    part = tmp_path / "f.csv.part"
    part.write_bytes(b"GARBAGE")
    try:
        fs.download(srv.url, tmp_path / "f.csv", fs.Budget(0), resume=True)
    finally:
        srv.httpd.shutdown()
    assert (tmp_path / "f.csv").read_bytes() == body


def test_bad_content_range_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    body = b"x" * 1000
    srv = _RangeServer(body, bad_range=True)
    part = tmp_path / "f.csv.part"
    part.write_bytes(body[:100])
    try:
        with pytest.raises(fs.IncompleteDownload):
            fs.download(srv.url, tmp_path / "f.csv", fs.Budget(0), resume=True)
    finally:
        srv.httpd.shutdown()
    assert not (tmp_path / "f.csv").exists()
    assert part.read_bytes() == body[:100]               # kept, not appended to


def test_total_change_between_attempts_is_fatal(tmp_path, monkeypatch):
    """Attempt 1: 1000-byte body cut at 300. Attempt 2: upstream now 1200 bytes."""
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    calls = {"n": 0}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            calls["n"] += 1
            if calls["n"] == 1:
                self.send_response(200)
                self.send_header("Content-Length", "1000")
                self.end_headers()
                self.wfile.write(b"a" * 300)
            else:
                self.send_response(206)
                self.send_header("Content-Range", "bytes 300-1199/1200")
                self.send_header("Content-Length", "900")
                self.end_headers()
                self.wfile.write(b"b" * 900)
            self.close_connection = True

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        with pytest.raises(fs.TotalChanged):
            fs.download(f"http://127.0.0.1:{httpd.server_address[1]}/f", tmp_path / "f",
                        fs.Budget(0))
    finally:
        httpd.shutdown()
    assert (tmp_path / "f.part").read_bytes() == b"a" * 300     # untouched, not spliced
    assert not (tmp_path / "f").exists()


def test_transient_http_errors_retry(tmp_path, monkeypatch):
    monkeypatch.setattr(fs.time, "sleep", lambda s: None)
    calls = {"n": 0}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            calls["n"] += 1
            if calls["n"] <= 2:
                self.send_error(503)
                return
            self.send_response(200)
            self.send_header("Content-Length", "5")
            self.end_headers()
            self.wfile.write(b"hello")

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        n, _ = fs.download(f"http://127.0.0.1:{httpd.server_address[1]}/f", tmp_path / "f",
                           fs.Budget(0))
    finally:
        httpd.shutdown()
    assert n == 5 and calls["n"] == 3


def test_folder_lock_blocks_second_fetcher(tmp_path):
    with fs.FolderLock(tmp_path):
        assert (tmp_path / ".fetch.lock").exists()
        with pytest.raises(fs.RefusedError, match="another fetcher"):
            with fs.FolderLock(tmp_path):
                pass
        assert (tmp_path / ".fetch.lock").exists()      # the loser never removes it
    assert not (tmp_path / ".fetch.lock").exists()


def test_mimic_record_list_plausibility(tmp_path):
    p = tmp_path / "record_list.csv"
    pd.DataFrame({"subject_id": [1, 1, 2], "study_id": [10, 11, 12], "file_name": ["a"] * 3,
                  "ecg_time": ["t"] * 3, "path": ["x"] * 3}).to_csv(p, index=False)
    r = fs.mimic_record_list_check(p)
    assert r["parses"] and r["rows"] == 3 and r["distinct_subject_id"] == 2
    assert r["missing_expected_columns"] == "none"
    p.write_text("not,a\n\"broken")
    assert fs.mimic_record_list_check(p)["parses"] in (True, False)   # never raises

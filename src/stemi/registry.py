"""Documentary dataset registry (data_contract §2.1, §2.3, V1, V2).

Every value here is a publisher-level registry entry copied from the PDFs,
not a measured inventory [MCR p.3]. Local observations live in
``stemi.inventory`` and never write back to this module (E2, E3, P3).
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

EVIDENCE_LEVEL = "documentary_publisher_level"  # E3: not an observation


@dataclass(frozen=True)
class RegistryEntry:
    dataset_id: str               # engine key [NB p.11-13]
    dataset_name: str
    release: str                  # exact release string (V1)
    publisher_ecg_count: int
    publisher_hz: int             # released rate as documented, not acquisition rate (P5)
    n_leads: int
    duration_s: str               # kept verbatim: ranges / "Unknown" are not coerced
    container: str
    source_ref: str
    technical_status: str         # §2.3, as of 10 Oct 2026; "Candidate" is not approval
    required_before_use: str
    duration_note: str | None = None
    evidence_level: str = EVIDENCE_LEVEL


_ENTRIES = (
    RegistryEntry("ptb_xl", "PTB-XL", "1.0.3, records500", 21_799, 500, 12, "10",
                  "WFDB-DAT", "[MCR p.3; NB p.10]", "Candidate",
                  "Check acquisition gaps; review acute timing and subtype evidence"),
    RegistryEntry("mimic_iv_ecg", "MIMIC-IV-ECG", "1.0", 800_035, 500, 12, "10",
                  "WFDB-DAT", "[MCR p.3; NB p.10]", "Hold",
                  "Verify amplitude calibration; review clinical linkage and adjudication"),
    RegistryEntry("ningbo", "Ningbo", "Challenge 2021 / 1.0.3", 34_905, 500, 12, "10",
                  "WFDB-MAT", "[MCR p.3; NB p.10]", "Hold",
                  "Verify calibration and acquisition details; review label meaning"),
    RegistryEntry("chapman_shaoxing", "Chapman-Shaoxing", "Challenge 2021 / 1.0.3", 10_247,
                  500, 12, "10", "WFDB-MAT", "[MCR p.3; NB p.10]", "Hold",
                  "Verify calibration; distinguish original and challenge exports"),
    RegistryEntry("georgia", "Georgia 12-lead", "Challenge 2021 / 1.0.3", 10_344, 500, 12,
                  "5–10", "WFDB-MAT", "[MCR p.3; NB p.10]", "Hold",
                  "Verify calibration and 5–10 s window policy; review patient linkage"),
    RegistryEntry("cpsc_2018", "CPSC 2018", "Challenge 2021 / 1.0.3", 6_877, 500, 12,
                  "6–144", "WFDB-MAT", "[MCR p.3; NB p.10]", "Hold",
                  "Verify calibration; define variable-duration policy",
                  duration_note="Range describes the combined CPSC source, not each subset [MCR p.3; NB p.15]"),
    RegistryEntry("cpsc_extra", "CPSC-Extra", "Challenge 2021 / 1.0.3", 3_453, 500, 12,
                  "6–144", "WFDB-MAT", "[MCR p.3; NB p.16]", "Hold",
                  "As CPSC 2018; review overlap with related CPSC exports",
                  duration_note="Range describes the combined CPSC source, not each subset [MCR p.3; NB p.15]"),
    RegistryEntry("sph", "Shandong Provincial Hospital", "Figshare collection 5779802 v1",
                  25_770, 500, 12, "10–60", "HDF5-record", "[MCR p.3; NB p.15–16]", "Candidate",
                  "Define duration policy; review AHA statements and acquisition gaps"),
    RegistryEntry("ptb_diagnostic", "PTB Diagnostic", "1.0.0 native", 549, 1000, 15, "Unknown",
                  "WFDB-DAT", "[MCR p.3; NB p.16]", "Candidate",
                  "Select standard 12 leads; plan 1000→500 Hz; verify duration"),
    RegistryEntry("incart", "INCART", "1.0.0 native", 75, 257, 12, "1800 (Holter)",
                  "WFDB-DAT", "[MCR p.3; CMP p.3]", "Hold",
                  "Review Holter domain and window-level eligibility before inclusion"),
    RegistryEntry("code15", "CODE-15%", "Zenodo 4916206", 345_779, 400, 12,
                  "7–10 (stored padded to 4096 samples)", "HDF5-shard", "[MCR p.3; NB p.16]",
                  "Hold",
                  "Verify amplitude scale, padding interpretation and target-label availability"),
)

# Read-only view: item assignment raises TypeError, entries are frozen (E3, P3).
REGISTRY: Mapping[str, RegistryEntry] = MappingProxyType({e.dataset_id: e for e in _ENTRIES})

DATASET_IDS: tuple[str, ...] = tuple(REGISTRY)

CHALLENGE_DATASET_IDS: tuple[str, ...] = (
    "ningbo", "chapman_shaoxing", "georgia", "cpsc_2018", "cpsc_extra",
)

# V2: pinned upstream assessment [MCR p.11; NB p.10; NB p.24].
UPSTREAM_PROVENANCE: Mapping[str, str] = MappingProxyType({
    "run_id": "metadata_compatibility_v1",
    "timestamp_utc": "2026-10-10T09:11:04Z",
    "engine_version": "1.0.0",
    "python": "3.13.16",
    "numpy": "2.1.3",
    "pandas": "2.2.3",
    "scipy": "1.16.3",
    "matplotlib": "3.10.0",
    "registry_curation_date": "2026-10-10",
    "registry_digest_location": "run_provenance.json",  # not in this repo (Q1)
})


class ReleaseMismatchError(ValueError):
    """A dataset reference used a release other than the registered one (V1, O3, O7)."""


def get_entry(dataset_id: str, release: str | None = None) -> RegistryEntry:
    """Return the registered entry; if ``release`` is given it must match exactly.

    O3/O7: other editions (e.g. the INCART Challenge subset, 74 records) are not
    registered here and are never silently resolved to the native entry.
    """
    if dataset_id not in REGISTRY:
        raise KeyError(f"unknown dataset_id {dataset_id!r}; use an engine key from §2.1")
    entry = REGISTRY[dataset_id]
    if release is not None and release != entry.release:
        raise ReleaseMismatchError(
            f"{dataset_id}: release {release!r} is not the registered {entry.release!r} (V1, O7)"
        )
    return entry

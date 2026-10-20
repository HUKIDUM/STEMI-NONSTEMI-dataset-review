import dataclasses

import pytest

from stemi.registry import (
    DATASET_IDS, EVIDENCE_LEVEL, REGISTRY, UPSTREAM_PROVENANCE, ReleaseMismatchError, get_entry,
)

EXPECTED = {
    # id: (release, count, hz, leads, duration, container, status)
    "ptb_xl": ("1.0.3, records500", 21_799, 500, 12, "10", "WFDB-DAT", "Candidate"),
    "mimic_iv_ecg": ("1.0", 800_035, 500, 12, "10", "WFDB-DAT", "Hold"),
    "ningbo": ("Challenge 2021 / 1.0.3", 34_905, 500, 12, "10", "WFDB-MAT", "Hold"),
    "chapman_shaoxing": ("Challenge 2021 / 1.0.3", 10_247, 500, 12, "10", "WFDB-MAT", "Hold"),
    "georgia": ("Challenge 2021 / 1.0.3", 10_344, 500, 12, "5–10", "WFDB-MAT", "Hold"),
    "cpsc_2018": ("Challenge 2021 / 1.0.3", 6_877, 500, 12, "6–144", "WFDB-MAT", "Hold"),
    "cpsc_extra": ("Challenge 2021 / 1.0.3", 3_453, 500, 12, "6–144", "WFDB-MAT", "Hold"),
    "sph": ("Figshare collection 5779802 v1", 25_770, 500, 12, "10–60", "HDF5-record", "Candidate"),
    "ptb_diagnostic": ("1.0.0 native", 549, 1000, 15, "Unknown", "WFDB-DAT", "Candidate"),
    "incart": ("1.0.0 native", 75, 257, 12, "1800 (Holter)", "WFDB-DAT", "Hold"),
    "code15": ("Zenodo 4916206", 345_779, 400, 12, "7–10 (stored padded to 4096 samples)",
               "HDF5-shard", "Hold"),
}


def test_exact_engine_keys():
    assert DATASET_IDS == tuple(EXPECTED)


@pytest.mark.parametrize("ds", list(EXPECTED))
def test_registry_values_match_contract(ds):
    e = REGISTRY[ds]
    got = (e.release, e.publisher_ecg_count, e.publisher_hz, e.n_leads,
           e.duration_s, e.container, e.technical_status)
    assert got == EXPECTED[ds]
    assert e.evidence_level == EVIDENCE_LEVEL == "documentary_publisher_level"
    assert e.source_ref.startswith("[") and e.required_before_use


def test_durations_not_coerced_to_numbers():
    assert all(isinstance(e.duration_s, str) for e in REGISTRY.values())
    assert REGISTRY["ptb_diagnostic"].duration_s == "Unknown"
    assert "combined" in REGISTRY["cpsc_2018"].duration_note


def test_registry_is_read_only():
    with pytest.raises(TypeError):
        REGISTRY["ptb_xl"] = None
    with pytest.raises(dataclasses.FrozenInstanceError):
        REGISTRY["ptb_xl"].publisher_hz = 250
    with pytest.raises(TypeError):
        UPSTREAM_PROVENANCE["engine_version"] = "2"


def test_ptb_xl_historical_count_never_used_for_1_0_3():  # O8
    e = get_entry("ptb_xl", "1.0.3, records500")
    assert e.publisher_ecg_count == 21_799
    assert all(v != 21_837 for v in dataclasses.asdict(e).values())


def test_incart_challenge_subset_not_merged():  # O3, O7
    e = get_entry("incart", "1.0.0 native")
    assert e.publisher_ecg_count == 75
    assert all(x.publisher_ecg_count != 74 for x in REGISTRY.values())
    with pytest.raises(ReleaseMismatchError):
        get_entry("incart", "Challenge 2021 / 1.0.3")


def test_unknown_release_or_key_rejected():  # V1
    with pytest.raises(ReleaseMismatchError):
        get_entry("ptb_xl", "1.0.3")  # records500 qualifier is part of the release string
    with pytest.raises(KeyError):
        get_entry("ptbxl")


def test_upstream_provenance_pinned():  # V2
    assert UPSTREAM_PROVENANCE["run_id"] == "metadata_compatibility_v1"
    assert UPSTREAM_PROVENANCE["timestamp_utc"] == "2026-10-10T09:11:04Z"
    assert UPSTREAM_PROVENANCE["engine_version"] == "1.0.0"
    assert UPSTREAM_PROVENANCE["python"] == "3.13.16"
    assert (UPSTREAM_PROVENANCE["numpy"], UPSTREAM_PROVENANCE["pandas"],
            UPSTREAM_PROVENANCE["scipy"], UPSTREAM_PROVENANCE["matplotlib"]) == (
        "2.1.3", "2.2.3", "1.16.3", "3.10.0")
    assert UPSTREAM_PROVENANCE["registry_curation_date"] == "2026-10-10"

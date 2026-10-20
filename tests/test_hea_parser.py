"""hea_parser on invented headers shaped like the documented layouts (no real data)."""

import pytest

from stemi.review.hea_parser import (
    header_row, parse_comment_fields, parse_header, parse_header_text, parse_signal_line,
)

LEADS = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]


def _hea(record_line, sig_fmt, leads, comments=()):
    lines = [record_line] + [sig_fmt.format(lead=lead) for lead in leads]
    return "\n".join(lines + [f"#{c}" for c in comments]) + "\n"


def test_challenge_style_header():
    text = _hea("A0001 12 500 7500 05-Feb-2020 11:39:16",
                "A0001.mat 16+24 1000/mV 16 0 28 -1716 0 {lead}", LEADS,
                ["Age: 74", "Sex: Male", "Dx: 59118001,164884008", "Rx: Unknown"])
    h = parse_header_text(text)
    assert (h.record_name, h.n_sig, h.fs, h.n_samples) == ("A0001", 12, 500.0, 7500)
    assert h.duration_s == 15.0
    assert h.lead_names == LEADS
    s = h.signals[0]
    assert (s.fmt, s.gain, s.baseline, s.units, s.adc_res, s.adc_zero) == ("16+24", 1000.0, None, "mV", 16, 0)
    assert h.comment_fields == {"Age": "74", "Sex": "Male", "Dx": "59118001,164884008",
                                "Rx": "Unknown"}


def test_ptb_diagnostic_style_15_leads_and_comments():
    leads = [l.lower() for l in LEADS] + ["vx", "vy", "vz"]
    text = _hea("s0010_re 15 1000 38400",
                "s0010_re.dat 16 2000 16 0 -489 -8337 0 {lead}", leads,
                [" age: 81", " sex: female", " Reason for admission: Myocardial infarction",
                 " Acute infarction (localization): infero-latera"])
    h = parse_header_text(text)
    assert h.n_sig == 15 and h.duration_s == 38.4
    assert h.signals[0].gain == 2000.0 and h.signals[0].units is None   # not given
    assert h.comment_fields["Reason for admission"] == "Myocardial infarction"
    assert h.comment_fields["Acute infarction (localization)"] == "infero-latera"


def test_gain_with_baseline_and_units():
    s = parse_signal_line("x.dat 16 200.5(-12)/uV 12 0 0 0 0 aVR")
    assert (s.gain, s.baseline, s.units, s.description) == (200.5, -12, "uV", "aVR")


def test_description_with_spaces_kept():
    s = parse_signal_line("x.dat 212 200 11 1024 995 -22131 0 MLII lead extra")
    assert s.description == "MLII lead extra"


def test_minimal_signal_line_leaves_fields_none():
    s = parse_signal_line("x.dat 16")
    assert s.gain is None and s.units is None and s.description is None


def test_fs_with_counter_frequency():
    h = parse_header_text(_hea("r 1 360/180(0) 100", "r.dat 16 200 16 0 0 0 0 {lead}", ["I"]))
    assert h.fs == 360.0 and h.counter_freq == 180.0


def test_missing_fs_gives_no_duration():
    h = parse_header_text("r 0\n")
    assert h.fs is None and h.duration_s is None


def test_wrong_signal_count_raises():
    with pytest.raises(ValueError):
        parse_header_text(_hea("r 3 500 5000", "r.dat 16 1000/mV 16 0 0 0 0 {lead}", ["I", "II"]))


def test_multisegment_refused():
    with pytest.raises(ValueError, match="multi-segment"):
        parse_header_text("r/2 1 250 1000\nseg1 500\nseg2 500\n")


def test_repeated_comment_key_keeps_all_values():
    assert parse_comment_fields(["Dx: a", "Dx: b", "no colon here"]) == {"Dx": "a | b"}


def test_header_row_and_file(tmp_path):
    p = tmp_path / "r.hea"
    p.write_text(_hea("r 2 500 5000", "r.dat 16 1000/mV 16 0 0 0 0 {lead}", ["I", "II"]))
    row = header_row(parse_header(p))
    assert row["lead_names"] == "I|II" and row["units"] == "mV" and row["duration_s"] == 10.0

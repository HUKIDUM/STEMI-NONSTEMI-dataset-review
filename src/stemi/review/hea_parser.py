"""WFDB ``.hea`` header parser for the dataset review (step S2).

Reads header text only, never sample files. Compared with
``stemi.inventory.parse_wfdb_header`` it also keeps per-signal gain, baseline,
units, format and ADC fields, and turns ``# key: value`` comments into pairs.

Header layout (WFDB "header" format):
    record line:  name[/nseg] n_sig [fs[/counter_freq[(base)]] [n_samples [time [date]]]]
    signal line:  file fmt[xspf][:skew][+offset] [gain[(baseline)][/units] [adc_res
                  [adc_zero [init_value [checksum [block_size [description]]]]]]]
    comments:     lines starting with '#'
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_GAIN = re.compile(r"^(?P<gain>[-+0-9.eE]+)(?:\((?P<baseline>-?\d+)\))?(?:/(?P<units>\S+))?$")


@dataclass
class Signal:
    file_name: str
    fmt: str
    gain: float | None = None           # ADC units per physical unit; None = not given
    baseline: int | None = None         # None = not given (WFDB default is adc_zero)
    units: str | None = None            # None = not given (WFDB default is mV)
    adc_res: int | None = None
    adc_zero: int | None = None
    init_value: int | None = None
    checksum: int | None = None
    block_size: int | None = None
    description: str | None = None      # lead name


@dataclass
class Header:
    record_name: str
    n_segments: int | None
    n_sig: int
    fs: float | None
    counter_freq: float | None
    n_samples: int | None
    base_time: str | None
    base_date: str | None
    signals: list[Signal] = field(default_factory=list)
    comments: list[str] = field(default_factory=list)
    comment_fields: dict[str, str] = field(default_factory=dict)

    @property
    def duration_s(self) -> float | None:
        if self.fs and self.n_samples is not None:
            return self.n_samples / self.fs
        return None

    @property
    def lead_names(self) -> list[str | None]:
        return [s.description for s in self.signals]


def _int(tok: str | None) -> int | None:
    return int(tok) if tok not in (None, "") else None


def parse_record_line(line: str) -> dict:
    tok = line.split()
    name, _, nseg = tok[0].partition("/")
    out = {"record_name": name, "n_segments": _int(nseg) if nseg else None,
           "n_sig": int(tok[1]), "fs": None, "counter_freq": None, "n_samples": None,
           "base_time": None, "base_date": None}
    if len(tok) > 2:
        fs, _, counter = tok[2].partition("/")
        out["fs"] = float(fs)
        if counter:
            out["counter_freq"] = float(counter.split("(")[0])
    if len(tok) > 3:
        out["n_samples"] = int(tok[3])
    if len(tok) > 4:
        out["base_time"] = tok[4]
    if len(tok) > 5:
        out["base_date"] = tok[5]
    return out


def parse_signal_line(line: str) -> Signal:
    tok = line.split(maxsplit=8)
    sig = Signal(file_name=tok[0], fmt=tok[1])
    if len(tok) > 2:
        m = _GAIN.match(tok[2])
        if not m:
            raise ValueError(f"cannot parse gain field {tok[2]!r}")
        sig.gain = float(m["gain"])
        sig.baseline = _int(m["baseline"])
        sig.units = m["units"]
    for attr, idx in (("adc_res", 3), ("adc_zero", 4), ("init_value", 5),
                      ("checksum", 6), ("block_size", 7)):
        if len(tok) > idx:
            setattr(sig, attr, int(tok[idx]))
    if len(tok) > 8:
        sig.description = tok[8].strip()
    return sig


def parse_comment_fields(comments: list[str]) -> dict[str, str]:
    """``Key: value`` comment lines -> dict. Keys keep their original spelling.

    A repeated key keeps every value, joined with `` | ``.
    """
    out: dict[str, str] = {}
    for c in comments:
        key, sep, value = c.partition(":")
        if not sep or not key.strip():
            continue
        key, value = key.strip(), value.strip()
        out[key] = f"{out[key]} | {value}" if key in out else value
    return out


def parse_header_text(text: str) -> Header:
    lines = text.splitlines()
    comments = [ln.lstrip("#").strip() for ln in lines if ln.lstrip().startswith("#")]
    body = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith("#")]
    if not body:
        raise ValueError("no record line")
    rec = parse_record_line(body[0])
    if rec["n_segments"]:
        raise ValueError("multi-segment headers are not supported")
    signals = [parse_signal_line(ln) for ln in body[1:1 + rec["n_sig"]]]
    if len(signals) != rec["n_sig"]:
        raise ValueError(f"expected {rec['n_sig']} signal lines, found {len(signals)}")
    return Header(**rec, signals=signals, comments=comments,
                  comment_fields=parse_comment_fields(comments))


def parse_header(path: Path) -> Header:
    return parse_header_text(Path(path).read_text(errors="replace"))


def header_row(h: Header) -> dict:
    """Flat summary row (one per header) for result tables."""
    def joined(attr):
        vals = {getattr(s, attr) for s in h.signals}
        return "|".join(sorted("" if v is None else str(v) for v in vals))
    return {
        "record_name": h.record_name, "n_sig": h.n_sig, "fs": h.fs,
        "n_samples": h.n_samples, "duration_s": h.duration_s,
        "lead_names": "|".join("" if n is None else n for n in h.lead_names),
        "gains": joined("gain"), "baselines": joined("baseline"),
        "units": joined("units"), "fmts": joined("fmt"), "adc_res": joined("adc_res"),
        "base_time": h.base_time, "base_date": h.base_date,
        "n_comments": len(h.comments),
    }

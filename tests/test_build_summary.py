"""build_summary on invented result/sample files (no real data)."""

import pandas as pd

from stemi.review import build_summary as bs


def test_rows_and_not_observed(tmp_path):
    r, s = tmp_path / "results", tmp_path / "samples"
    r.mkdir()
    (s / "ptb_xl").mkdir(parents=True)
    pd.DataFrame({"ecg_id": [1, 2, 3], "patient_id": [7, 7, 8]}).to_csv(s / "ptb_xl" / "ptbxl_database.csv", index=False)
    pd.DataFrame({"selection": ["any listed MI/injury code",
                                "any listed code AND stadium1 or stadium2 in ['Stadium I', 'Stadium I-II']"],
                  "n_ecgs": [2, 1], "n_patients": [2, 1]}).to_csv(r / "ptb_xl_mi_early_stadium.csv", index=False)
    df = bs.build(r, s).set_index("dataset_id")
    assert list(df.columns) == bs.COLUMNS[1:]
    assert df.loc["ptb_xl", "ecgs"] == "3" and df.loc["ptb_xl", "patients"] == "2"
    assert df.loc["ptb_xl", "mi_related_ecgs"] == 2
    assert df.loc["sph", "ecgs"] == bs.NA                     # nothing downloaded -> not observed
    assert (r / "dataset_summary.csv").exists()

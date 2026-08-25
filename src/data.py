"""
Data loading for the India education gap analysis.

PRIMARY DATA SOURCE:
    UDISE (Unified District Information System for Education), 2015-16 state
    report — school-, teacher-, and examination-level counts collected by
    India's Ministry of Education. This is the same underlying administrative
    census UDISE+ continues today.

ACCESSED VIA:
    A public mirror of the raw 2015-16 UDISE state/district tables
    ("Education in India", Kaggle, uploaded by rajanand), which cites MHRD/DISE
    as its source. See docs/DATA_SOURCES.md for the full citation and how to
    refresh this file from a newer UDISE+ release.

This is real, single-year (2015-16) administrative data, not a survey
estimate or a synthetic sample. It is a cross-section: one snapshot in time,
not a multi-year trend.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "2015_16_Statewise_Secondary.csv"

# Columns needed to compute pupil-teacher ratio and the class-10 pass rate.
_PTR_COLS = ["enr_all", "tch_all"]
_APR_PY10_COLS = [
    "apr_b_gen_py10", "apr_g_gen_py10", "apr_b_sc_py10", "apr_g_sc_py10",
    "apr_b_st_py10", "apr_g_st_py10", "apr_b_obc_py10", "apr_g_obc_py10",
]
_PASS_PY10_COLS = [
    "pass_b_gen_py10", "pass_g_gen_py10", "pass_b_sc_py10", "pass_g_sc_py10",
    "pass_b_st_py10", "pass_g_st_py10", "pass_b_obc_py10", "pass_g_obc_py10",
]


def load_states() -> pd.DataFrame:
    """Load and clean the state-level 2015-16 UDISE secondary-education table.

    Returns one row per state/UT with:
      state, literacy_rate, male_literacy_rate, female_literacy_rate,
      gender_gap, pupil_teacher_ratio, class10_appeared, class10_passed,
      class10_pass_rate
    """
    cols = ["statname", "literacy_rate", "male_literacy_rate", "female_literacy_rate"]
    cols += _PTR_COLS + _APR_PY10_COLS + _PASS_PY10_COLS
    df = pd.read_csv(DATA, encoding="latin-1", usecols=cols)

    df["state"] = df["statname"].str.strip().str.title()
    df = df.drop(columns=["statname"])

    for col in ["literacy_rate", "male_literacy_rate", "female_literacy_rate"] + _PTR_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["gender_gap"] = (df["male_literacy_rate"] - df["female_literacy_rate"]).round(1)
    df["pupil_teacher_ratio"] = (df["enr_all"] / df["tch_all"]).round(1)

    df["class10_appeared"] = df[_APR_PY10_COLS].sum(axis=1)
    df["class10_passed"] = df[_PASS_PY10_COLS].sum(axis=1)
    df["class10_pass_rate"] = (
        df["class10_passed"] / df["class10_appeared"] * 100
    ).round(1)

    # A handful of UTs report zero appeared/passed (exams run by a different
    # board or not captured this cycle) -- treat as missing rather than a
    # real 0% pass rate.
    df.loc[df["class10_appeared"] == 0, "class10_pass_rate"] = pd.NA

    df = df[df["literacy_rate"].between(0, 100)]
    df = df[df["pupil_teacher_ratio"].between(0, 100)]

    keep = ["state", "literacy_rate", "male_literacy_rate", "female_literacy_rate",
            "gender_gap", "pupil_teacher_ratio", "class10_appeared",
            "class10_passed", "class10_pass_rate"]
    return df[keep].reset_index(drop=True)


if __name__ == "__main__":
    states = load_states()
    print(f"Loaded {len(states)} states/UTs")
    print(states.describe(include="all"))

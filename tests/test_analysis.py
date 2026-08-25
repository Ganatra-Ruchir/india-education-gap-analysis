"""
Tests for the India education gap analysis.  Run:  pytest -q
"""
from pathlib import Path
import sys
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import data as data_mod  # noqa: E402


@pytest.fixture(scope="module")
def states():
    return data_mod.load_states()


def test_expected_columns_present(states):
    expected = {"state", "literacy_rate", "male_literacy_rate", "female_literacy_rate",
                "gender_gap", "pupil_teacher_ratio", "class10_appeared",
                "class10_passed", "class10_pass_rate"}
    assert expected.issubset(states.columns)


def test_literacy_and_ptr_are_bounded(states):
    assert states["literacy_rate"].between(0, 100).all()
    assert states["pupil_teacher_ratio"].between(0, 100).all()


def test_gender_gap_matches_manual_calc(states):
    manual = (states["male_literacy_rate"] - states["female_literacy_rate"]).round(1)
    assert np.allclose(states["gender_gap"], manual)


def test_pass_rate_matches_manual_calc(states):
    have_data = states.dropna(subset=["class10_pass_rate"])
    manual = (have_data["class10_passed"] / have_data["class10_appeared"] * 100).round(1)
    assert np.allclose(have_data["class10_pass_rate"], manual)


def test_zero_appeared_is_missing_not_zero_percent(states):
    zero_appeared = states[states["class10_appeared"] == 0]
    assert zero_appeared["class10_pass_rate"].isna().all()


def test_no_duplicate_states(states):
    assert states["state"].is_unique


def test_telangana_excluded_for_missing_literacy():
    """Telangana is dropped upstream because its literacy figures are NaN in
    this release (it split from Andhra Pradesh in 2014) -- this should stay
    a documented data gap, not silently reappear as a 0 or fabricated value.
    """
    states = data_mod.load_states()
    assert "Telangana" not in set(states["state"])

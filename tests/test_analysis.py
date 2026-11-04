import numpy as np
import pandas as pd
import pytest

from capitaldynamics.analysis.acquisition import analyze_capital_acquisition
from capitaldynamics.analysis.retirement import analyze_capital_retirement
from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.preparation.datasets import (
    DataContractError,
    prepare_acquisition_data,
    prepare_retirement_data,
)


@pytest.fixture
def observations() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "real_investment": [10.0, 11.0, 12.0, 13.0],
            "nominal_gdp": [100.0, 110.0, 120.0, 130.0],
            "real_gdp": [100.0, 105.0, 110.0, 115.0],
            "full_capacity_real_gdp": [110.0, 116.0, 122.0, 128.0],
            "real_fixed_assets": [50.0, 53.0, 55.0, 58.0],
            "manufacturing_labor": [20.0, 21.0, 22.0, 23.0],
        },
        index=pd.Index([2000, 2001, 2002, 2003], name="year"),
    )


def test_acquisition_formulas_and_gamma_switch(
    observations: pd.DataFrame,
) -> None:
    prepared = prepare_acquisition_data(observations)
    schedule = GammaSchedule.from_pairs([(2000, 0.5), (2002, 1.0)])
    result = analyze_capital_acquisition(prepared, schedule)
    assert result["year"].tolist() == [2000, 2001, 2002, 2003]
    assert np.isnan(result.loc[0, "estimates"])
    # Transition 2000->2001 uses source-year Gamma 0.5 and destination I[2001].
    assert result.loc[1, "estimates"] == pytest.approx(3.0 + 0.5 * 11.0)
    # Transition 2001->2002 still uses Gamma 0.5; switch starts in 2002.
    assert result.loc[2, "estimates"] == pytest.approx(2.0 + 0.5 * 12.0)
    # Transition 2002->2003 uses Gamma 1.0.
    assert result.loc[3, "estimates"] == pytest.approx(3.0 + 1.0 * 13.0)


def test_retirement_preserves_current_python_equation(
    observations: pd.DataFrame,
) -> None:
    prepared = prepare_retirement_data(observations)
    schedule = GammaSchedule.from_pairs([(2000, 0.5)])
    result = analyze_capital_retirement(prepared, schedule)
    # K[t] - K[t+1] + Gamma[t] * I[t], divided by K[t+1].
    expected_value = 50.0 - 53.0 + 0.5 * 10.0
    assert np.isnan(result.loc[0, "retirement_values"])
    assert result.loc[1, "retirement_values"] == pytest.approx(expected_value)
    assert result.loc[1, "retirement_ratios"] == pytest.approx(
        expected_value / 53.0
    )


def test_retirement_can_start_at_selected_year(
    observations: pd.DataFrame,
) -> None:
    prepared = prepare_retirement_data(observations, start_year=2001)
    assert prepared.frame.index.tolist() == [2001, 2002, 2003]
    # The deflator base year is searched in the complete source series, not
    # incorrectly re-searched after slicing.
    assert prepared.deflator_base_year == 2000


def test_invalid_missing_deflator_base_year_fails_clearly(
    observations: pd.DataFrame,
) -> None:
    invalid = observations.copy()
    invalid["nominal_gdp"] = invalid["nominal_gdp"] + 10.0
    with pytest.raises(
        DataContractError, match="Could not identify a GDP-deflator"
    ):
        prepare_acquisition_data(invalid)


def test_gamma_schedule_must_cover_first_year_and_switch_at_observed_year(
    observations: pd.DataFrame,
) -> None:
    prepared = prepare_acquisition_data(observations)
    with pytest.raises(ValueError, match="first Gamma breakpoint"):
        analyze_capital_acquisition(
            prepared,
            GammaSchedule.from_pairs([(2001, 0.5)]),
        )
    with pytest.raises(ValueError, match="observed source year"):
        analyze_capital_acquisition(
            prepared,
            GammaSchedule.from_pairs([(2000, 0.5), (2003, 1.0)]),
        )


def test_unsorted_years_are_rejected(observations: pd.DataFrame) -> None:
    invalid = observations.iloc[::-1]
    with pytest.raises(DataContractError, match="strictly increasing"):
        prepare_acquisition_data(invalid)


def test_missing_annual_observation_is_rejected(
    observations: pd.DataFrame,
) -> None:
    invalid = observations.drop(index=2001)
    with pytest.raises(DataContractError, match="must be consecutive"):
        prepare_acquisition_data(invalid)

import numpy as np
import pandas as pd

from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.preparation.datasets import PreparedDataset


def analyze_capital_acquisition(
    dataset: PreparedDataset,
    gamma_schedule: GammaSchedule,
) -> pd.DataFrame:
    """Calculate acquisition indicators from validated observations.
    The calculation preserves the current Python implementation's formulas.
    Gamma is selected by the source year of each transition; the investment
    input in the acquisition estimate is the destination-year investment.
    """
    frame = dataset.frame
    years = frame.index.to_numpy(dtype=int)
    gamma_schedule.validate_for(years.tolist())
    investment = frame["real_investment"].to_numpy(dtype=float)
    real_output = frame["real_gdp"].to_numpy(dtype=float)
    full_capacity_output = frame["full_capacity_real_gdp"].to_numpy(
        dtype=float
    )
    capital = frame["real_fixed_assets"].to_numpy(dtype=float)
    labor = frame["manufacturing_labor"].to_numpy(dtype=float)
    # Static indicators. Their reference values are the first analysis year.
    observed_turnover = real_output / capital
    investment_output_index = (
        investment * real_output[0] / (investment[0] * real_output)
    )
    capital_intensity_index = capital * labor[0] / (capital[0] * labor)
    observed_labor_productivity = (
        real_output * labor[0] / (real_output[0] * labor)
    )
    log_capital_intensity = np.log(capital_intensity_index)
    log_observed_productivity = np.log(observed_labor_productivity)
    full_capacity_turnover = full_capacity_output / capital
    full_capacity_investment_output_index = (
        investment
        * full_capacity_output[0]
        / (investment[0] * full_capacity_output)
    )
    full_capacity_labor_productivity = (
        full_capacity_output * labor[0] / (full_capacity_output[0] * labor)
    )
    log_full_capacity_productivity = np.log(full_capacity_labor_productivity)
    # Dynamic acquisition estimate: ΔK[t] + Gamma[source year] * I[t].
    estimates = np.full(len(years), np.nan, dtype=float)
    for destination_position in range(1, len(years)):
        source_year = int(years[destination_position - 1])
        gamma = gamma_schedule.for_source_year(source_year)
        estimates[destination_position] = (
            capital[destination_position]
            - capital[destination_position - 1]
            + gamma * investment[destination_position]
        )
    return pd.DataFrame(
        {
            "year": years,
            "observed_turnover": observed_turnover,
            "investment_output_index": investment_output_index,
            "capital_intensity_index": capital_intensity_index,
            "observed_labor_productivity": observed_labor_productivity,
            "log_capital_intensity": log_capital_intensity,
            "log_observed_productivity": log_observed_productivity,
            "full_capacity_turnover": full_capacity_turnover,
            "full_capacity_investment_output_index": (
                full_capacity_investment_output_index
            ),
            "full_capacity_labor_productivity": (
                full_capacity_labor_productivity
            ),
            "log_full_capacity_productivity": log_full_capacity_productivity,
            "estimates": estimates,
        }
    )

import numpy as np
import pandas as pd

from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.preparation.datasets import PreparedDataset


def analyze_capital_retirement(
    dataset: PreparedDataset,
    gamma_schedule: GammaSchedule,
) -> pd.DataFrame:
    """Calculate capital-retirement indicators from validated observations.
    This intentionally preserves the current Python model's dynamic
    convention: for the transition from year t to t+1,
        retirement_value[t+1] = K[t] - K[t+1] + Gamma[t] * I[t]
    and the ratio is divided by end-period capital K[t+1]. This differs from
    the acquisition model's sign and investment-period convention; see the
    project README before changing either equation.
    """
    frame = dataset.frame
    years = frame.index.to_numpy(dtype=int)
    gamma_schedule.validate_for(years.tolist())
    investment = frame["real_investment"].to_numpy(dtype=float)
    real_output = frame["real_gdp"].to_numpy(dtype=float)
    capital = frame["real_fixed_assets"].to_numpy(dtype=float)
    labor = frame["manufacturing_labor"].to_numpy(dtype=float)
    log_capital_intensity = np.log(capital * labor[0] / (capital[0] * labor))
    log_labor_productivity = np.log(
        real_output * labor[0] / (real_output[0] * labor)
    )
    investment_output_index = (
        investment * real_output[0] / (investment[0] * real_output)
    )
    fixed_assets_turnover = real_output / capital
    retirement_values = np.full(len(years), np.nan, dtype=float)
    retirement_ratios = np.full(len(years), np.nan, dtype=float)
    for source_position in range(len(years) - 1):
        source_year = int(years[source_position])
        gamma = gamma_schedule.for_source_year(source_year)
        destination_position = source_position + 1
        value = (
            capital[source_position]
            - capital[destination_position]
            + gamma * investment[source_position]
        )
        retirement_values[destination_position] = value
        retirement_ratios[destination_position] = (
            value / capital[destination_position]
        )
    ratio_series = pd.Series(retirement_ratios, dtype=float)
    mean_ratio = float(ratio_series.mean(skipna=True))
    deviation_from_mean = np.abs(retirement_ratios - mean_ratio)
    return pd.DataFrame(
        {
            "year": years,
            "log_capital_intensity": log_capital_intensity,
            "log_labor_productivity": log_labor_productivity,
            "investment_output_index": investment_output_index,
            "fixed_assets_turnover": fixed_assets_turnover,
            "retirement_values": retirement_values,
            "retirement_ratios": retirement_ratios,
            "deviation_from_mean": deviation_from_mean,
        }
    )

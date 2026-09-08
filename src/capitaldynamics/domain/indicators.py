import numpy as np
import pandas as pd


def normalized_ratio(
    numerator: pd.Series, denominator: pd.Series, start: int
) -> pd.Series:
    ratio = numerator / denominator
    baseline = ratio.iloc[start]
    if not np.isfinite(baseline) or baseline == 0:
        raise ValueError("Normalization baseline must be finite and non-zero")
    return ratio / baseline


def static_indicators(
    frame: pd.DataFrame, start: int, include_maximum: bool
) -> pd.DataFrame:
    result = frame.copy()
    result["capital_turnover"] = result["real_gdp"] / result["real_capital"]
    result["investment_to_output"] = normalized_ratio(
        result["real_investment"], result["real_gdp"], start
    )
    result["capital_intensity"] = normalized_ratio(
        result["real_capital"], result["labor"], start
    )
    result["labor_productivity"] = normalized_ratio(
        result["real_gdp"], result["labor"], start
    )
    result["log_capital_intensity"] = np.log(result["capital_intensity"])
    result["log_labor_productivity"] = np.log(result["labor_productivity"])
    if include_maximum:
        if "maximum_output" not in result:
            raise ValueError(
                "capacity_utilization is required for acquisition analysis"
            )
        result["maximum_capital_turnover"] = (
            result["maximum_output"] / result["real_capital"]
        )
        result["maximum_investment_to_output"] = normalized_ratio(
            result["real_investment"], result["maximum_output"], start
        )
        result["maximum_labor_productivity"] = normalized_ratio(
            result["maximum_output"], result["labor"], start
        )
        result["maximum_log_labor_productivity"] = np.log(
            result["maximum_labor_productivity"]
        )
    return result

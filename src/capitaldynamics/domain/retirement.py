from dataclasses import dataclass

import numpy as np
import pandas as pd

from .indicators import static_indicators
from .models import CapitalDataset
from .schedule import GammaSchedule


@dataclass(frozen=True)
class RetirementResult:
    """Complete retirement-model result."""

    data: pd.DataFrame
    analysis_start: int
    base_year: int
    gamma: GammaSchedule

    def table(self) -> pd.DataFrame:
        return self.data.copy()


def calculate_retirement(
    dataset: CapitalDataset, analysis_start: int, gamma: GammaSchedule
) -> RetirementResult:
    frame = dataset.enriched()
    matches = frame.index[frame["period"] == analysis_start]
    if len(matches) == 0:
        raise ValueError(
            f"analysis_start {analysis_start} is not present in the dataset"
        )
    frame = frame.loc[matches[0] :].reset_index(drop=True)
    result = static_indicators(frame, start=0, include_maximum=False)
    result["retirement_value"] = np.nan
    result["retirement_ratio"] = np.nan
    for i, period in enumerate(result["period"].iloc[:-1]):
        try:
            gamma_value = gamma.for_period(int(period))
        except KeyError as exc:
            raise ValueError(str(exc)) from exc
        retirement_value = (
            result.loc[i, "real_capital"]
            - result.loc[i + 1, "real_capital"]
            + gamma_value * result.loc[i, "real_investment"]
        )
        result.loc[i, "retirement_value"] = retirement_value
        result.loc[i, "retirement_ratio"] = (
            retirement_value / result.loc[i + 1, "real_capital"]
        )
    result["retirement_ratio_deviation_abs"] = (
        result["retirement_ratio"] - result["retirement_ratio"].mean()
    ).abs()
    result["retirement_ratio_increment_abs"] = (
        result["retirement_ratio"].diff().abs()
    )
    return RetirementResult(result, analysis_start, dataset.base_year(), gamma)

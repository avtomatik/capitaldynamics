from dataclasses import dataclass

import numpy as np
import pandas as pd

from .indicators import static_indicators
from .models import CapitalDataset
from .schedule import GammaSchedule


@dataclass(frozen=True)
class AcquisitionResult:
    """Complete acquisition-model result."""

    data: pd.DataFrame
    analysis_start: int
    base_year: int
    gamma: GammaSchedule

    def table(self) -> pd.DataFrame:
        return self.data.copy()


def calculate_acquisition(
    dataset: CapitalDataset, analysis_start: int, gamma: GammaSchedule
) -> AcquisitionResult:
    frame = dataset.enriched()
    start_pos = (
        int(frame.index[frame["year"] == analysis_start][0])
        if (frame["year"] == analysis_start).any()
        else -1
    )
    if start_pos < 0:
        raise ValueError(
            f"analysis_start {analysis_start} is not present in the dataset"
        )
    frame = frame.loc[start_pos:].reset_index(drop=True)
    if "maximum_output" not in frame:
        raise ValueError("Acquisition analysis requires capacity_utilization")
    result = static_indicators(frame, start=0, include_maximum=True)
    result["capital_acquisition"] = np.nan
    # Historical Excel semantics: the estimate is labeled by the target year.
    # For target year t, use K_t - K_(t-1) + Gamma_t * I_t.
    for i in range(1, len(result)):
        target_period = int(result.loc[i, "year"])
        try:
            gamma_value = gamma.for_period(target_period)
        except KeyError as exc:
            raise ValueError(str(exc)) from exc
        result.loc[i, "capital_acquisition"] = (
            result.loc[i, "real_capital"]
            - result.loc[i - 1, "real_capital"]
            + gamma_value * result.loc[i, "real_investment"]
        )
    return AcquisitionResult(
        result, analysis_start, dataset.base_year(), gamma
    )

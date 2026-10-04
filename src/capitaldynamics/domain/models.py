from dataclasses import dataclass
from typing import Final

import pandas as pd

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    "year",
    "nominal_gdp",
    "real_gdp",
    "nominal_investment",
    "nominal_capital",
    "labor",
)


@dataclass(frozen=True)
class CapitalDataset:
    """Validated economic time series used by the capital models."""

    frame: pd.DataFrame

    def __post_init__(self) -> None:
        frame = self.frame.copy()
        missing = [c for c in REQUIRED_COLUMNS if c not in frame.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        frame = frame.sort_values("year").reset_index(drop=True)
        if frame["year"].duplicated().any():
            raise ValueError("year must contain unique observations")
        if len(frame) < 2:
            raise ValueError("At least two annual observations are required")
        if not frame["year"].is_monotonic_increasing:
            raise ValueError("year must be increasing")
        numeric = [c for c in REQUIRED_COLUMNS if c != "year"]
        for column in numeric:
            values = pd.to_numeric(frame[column], errors="coerce")
            if values.isna().any():
                raise ValueError(
                    f"Column {column!r} contains missing or non-numeric values"
                )
            frame[column] = values
        frame["year"] = pd.to_numeric(frame["year"], errors="raise")
        if (frame["real_gdp"] <= 0).any() or (frame["nominal_gdp"] == 0).any():
            raise ValueError(
                "GDP values must permit a positive finite deflator"
            )
        if (frame["labor"] <= 0).any():
            raise ValueError("labor must be positive")
        object.__setattr__(self, "frame", frame)

    @classmethod
    def from_frame(cls, frame: pd.DataFrame) -> "CapitalDataset":
        return cls(frame.copy())

    @property
    def periods(self) -> pd.Index:
        return pd.Index(self.frame["year"], name="year")

    def slice_from(self, start_period: int) -> "CapitalDataset":
        result = self.frame.loc[self.frame["year"] >= start_period].copy()
        if len(result) < 2:
            raise ValueError(
                "The analysis window must contain at least two observations"
            )
        return CapitalDataset(result)

    def base_year(self) -> int:
        deflator_gap = (
            self.frame["nominal_gdp"] / self.frame["real_gdp"] - 1.0
        ).abs()
        return int(self.frame.loc[deflator_gap.idxmin(), "year"])

    def enriched(self) -> pd.DataFrame:
        result = self.frame.copy()
        result["gdp_deflator"] = result["real_gdp"] / result["nominal_gdp"]
        result["real_investment"] = (
            result["nominal_investment"] * result["gdp_deflator"]
        )
        result["real_capital"] = (
            result["nominal_capital"] * result["gdp_deflator"]
        )
        if "capacity_utilization" in result:
            result["maximum_output"] = (
                result["real_gdp"] / result["capacity_utilization"]
            )
        return result

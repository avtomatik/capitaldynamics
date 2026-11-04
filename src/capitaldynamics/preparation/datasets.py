from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
import pandas as pd

ACQUISITION_COLUMNS = (
    "real_investment",
    "nominal_gdp",
    "real_gdp",
    "full_capacity_real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
)
RETIREMENT_COLUMNS = (
    "real_investment",
    "nominal_gdp",
    "real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
)


class DataContractError(ValueError):
    """Raised when source observations violate the analysis data contract."""


@dataclass(frozen=True)
class PreparedDataset:
    """Validated observations plus the latest GDP-deflator reference year."""

    frame: pd.DataFrame
    deflator_base_year: int


def find_deflator_base_year(
    frame: pd.DataFrame,
    *,
    tolerance: float = 1.0,
) -> int:
    """
    Return the latest year where nominal and real GDP agree within tolerance.
    This preserves the historical workbook's absolute-difference convention,
    while replacing an unbounded backwards loop with an explicit failure.
    """
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError(
            "Deflator tolerance must be a finite, non-negative number."
        )
    difference = frame["nominal_gdp"].to_numpy(dtype=float) - frame[
        "real_gdp"
    ].to_numpy(dtype=float)
    matches = np.flatnonzero(np.abs(difference) <= tolerance)
    if matches.size == 0:
        raise DataContractError(
            "Could not identify a GDP-deflator base year: no observation has "
            f"|nominal_gdp - real_gdp| <= {tolerance:g}."
        )
    return int(frame.index[matches[-1]])


def _normalise_year_index(frame: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame):
        raise DataContractError(
            "Input observations must be a pandas DataFrame."
        )
    if frame.empty:
        raise DataContractError("Input observations are empty.")
    source = frame.copy()
    if "year" in source.columns and source.index.name != "year":
        source = source.set_index("year")
    try:
        numeric_years = pd.to_numeric(pd.Index(source.index), errors="raise")
        year_values = np.asarray(numeric_years, dtype=float)
    except (TypeError, ValueError) as exc:
        raise DataContractError(
            "The observations must have a numeric year index or "
            "a 'year' column."
        ) from exc
    if not np.isfinite(year_values).all():
        raise DataContractError("Year values must be finite.")
    if not np.equal(year_values, np.floor(year_values)).all():
        raise DataContractError("Year values must be whole numbers.")
    years = year_values.astype(np.int64)
    if len(np.unique(years)) != len(years):
        raise DataContractError("Each year must occur exactly once.")
    year_steps = np.diff(years)
    if np.any(year_steps <= 0):
        raise DataContractError(
            "Observations must be ordered by strictly increasing year. "
            "The loader orders warehouse results automatically."
        )
    if np.any(year_steps != 1):
        gaps = [
            f"{int(years[position])} to {int(years[position + 1])}"
            for position, step in enumerate(year_steps)
            if step != 1
        ]
        raise DataContractError(
            "Annual observations must be consecutive; gaps were found between "
            f"{gaps[:10]!r}. "
            "Do not interpret multi-year changes as annual transitions."
        )
    source.index = pd.Index(years, name="year")
    return source


def _prepare(
    frame: pd.DataFrame,
    required_columns: Iterable[str],
    *,
    tolerance: float,
    deflator_base_year: int | None = None,
) -> PreparedDataset:
    source = _normalise_year_index(frame)
    required = tuple(required_columns)
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise DataContractError(
            "The input dataset is missing required columns: "
            f"{', '.join(missing)}."
        )
    prepared = source.loc[:, list(required)].copy()
    for column in required:
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")
        values = prepared[column].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            bad_years = prepared.index[~np.isfinite(values)].tolist()
            raise DataContractError(
                f"Column {column!r} contains null or non-finite values at "
                f"years {bad_years[:10]!r}."
            )
    if len(prepared) < 2:
        raise DataContractError(
            "At least two annual observations "
            "are required for transition analysis."
        )
    positive_columns = [
        "nominal_gdp",
        "real_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ]
    if "full_capacity_real_gdp" in prepared.columns:
        positive_columns.append("full_capacity_real_gdp")
    for column in positive_columns:
        invalid = prepared[column] <= 0
        if invalid.any():
            years = prepared.index[invalid].tolist()
            raise DataContractError(
                f"Column {column!r} must be strictly positive; invalid years: "
                f"{years[:10]!r}."
            )
    if np.isclose(float(prepared["real_investment"].iloc[0]), 0.0):
        raise DataContractError(
            "Real investment in the first analysis year must be non-zero "
            "because investment/output indices are normalised to that value."
        )
    base_year = (
        int(deflator_base_year)
        if deflator_base_year is not None
        else find_deflator_base_year(prepared, tolerance=tolerance)
    )
    return PreparedDataset(frame=prepared, deflator_base_year=base_year)


def prepare_acquisition_data(
    frame: pd.DataFrame,
    *,
    deflator_tolerance: float = 1.0,
) -> PreparedDataset:
    """
    Validate and select the source series required by acquisition analysis.
    """
    return _prepare(
        frame,
        ACQUISITION_COLUMNS,
        tolerance=deflator_tolerance,
    )


def prepare_retirement_data(
    frame: pd.DataFrame,
    *,
    start_year: int | None = None,
    deflator_tolerance: float = 1.0,
) -> PreparedDataset:
    """
    Validate retirement inputs, optionally starting at a selected base year.
    """
    source = _normalise_year_index(frame)
    missing = [
        column for column in RETIREMENT_COLUMNS if column not in source.columns
    ]
    if missing:
        raise DataContractError(
            "The input dataset is missing required columns: "
            f"{', '.join(missing)}."
        )
    base_values = source.loc[:, ["nominal_gdp", "real_gdp"]].copy()
    for column in ("nominal_gdp", "real_gdp"):
        base_values[column] = pd.to_numeric(
            base_values[column], errors="coerce"
        )
        if not np.isfinite(base_values[column].to_numpy(dtype=float)).all():
            raise DataContractError(
                f"Column {column!r} contains null or non-finite values; "
                "cannot identify the GDP-deflator base year."
            )
    base_year = find_deflator_base_year(
        base_values, tolerance=deflator_tolerance
    )
    if start_year is not None:
        start_year = int(start_year)
        if start_year not in source.index:
            raise DataContractError(
                f"Start year {start_year} is not present "
                "in the source observations."
            )
        source = source.loc[start_year:].copy()
    return _prepare(
        source,
        RETIREMENT_COLUMNS,
        tolerance=deflator_tolerance,
        deflator_base_year=base_year,
    )

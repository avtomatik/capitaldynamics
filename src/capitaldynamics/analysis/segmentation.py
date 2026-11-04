import math
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class GammaBreakpoint:
    """A Gamma value that becomes active from ``start_year`` onward."""

    start_year: int
    gamma: float

    def __post_init__(self) -> None:
        if (
            isinstance(self.start_year, bool)
            or int(self.start_year) != self.start_year
        ):
            raise ValueError("Gamma breakpoint years must be integers.")
        if not math.isfinite(float(self.gamma)):
            raise ValueError("Gamma values must be finite numbers.")


@dataclass(frozen=True)
class GammaSchedule:
    """Piecewise-constant Gamma values over source-year transitions.
    A breakpoint applies to the transition starting in that year. For example,
    breakpoints ``1947=0.9`` and ``1970=1.1`` mean that 0.9 is used for
    transitions with source years 1947 through 1969, and 1.1 from 1970 onward.
    """

    breakpoints: tuple[GammaBreakpoint, ...]

    def __post_init__(self) -> None:
        if not self.breakpoints:
            raise ValueError("At least one Gamma breakpoint is required.")
        years = [item.start_year for item in self.breakpoints]
        if years != sorted(years) or len(set(years)) != len(years):
            raise ValueError(
                "Gamma breakpoints must have unique, "
                "strictly increasing years."
            )

    @classmethod
    def from_pairs(cls, pairs: list[tuple[int, float]]) -> "GammaSchedule":
        return cls(
            tuple(
                GammaBreakpoint(int(year), float(value))
                for year, value in pairs
            )
        )

    def validate_for(self, years: list[int] | tuple[int, ...]) -> None:
        if len(years) < 2:
            raise ValueError(
                "At least two years are required for Gamma scheduling."
            )
        valid_source_years = set(int(year) for year in years[:-1])
        first_year = int(years[0])
        if self.breakpoints[0].start_year != first_year:
            raise ValueError(
                "The first Gamma breakpoint must equal the first analysis "
                f"year ({first_year})."
            )
        invalid = [
            item.start_year
            for item in self.breakpoints
            if item.start_year not in valid_source_years
        ]
        if invalid:
            raise ValueError(
                "Each Gamma breakpoint must be an observed source year with a "
                "following observation; invalid breakpoint years: "
                f"{invalid!r}."
            )

    def for_source_year(self, year: int) -> float:
        active = self.breakpoints[0].gamma
        for item in self.breakpoints:
            if item.start_year > year:
                break
            active = item.gamma
        return float(active)

    def as_records(self, last_year: int) -> list[dict[str, int | float]]:
        """
        Return display-ready ranges; each end is the next start or last year.
        """
        records: list[dict[str, int | float]] = []
        for position, item in enumerate(self.breakpoints):
            end_year = (
                self.breakpoints[position + 1].start_year
                if position + 1 < len(self.breakpoints)
                else int(last_year)
            )
            records.append(
                {
                    "start_year": item.start_year,
                    "end_year_exclusive": end_year,
                    "gamma": float(item.gamma),
                }
            )
        return records

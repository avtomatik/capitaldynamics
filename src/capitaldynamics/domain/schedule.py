import math
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class GammaSpan:
    """Inclusive transition-year span for a Gamma value."""

    start: int
    end: int
    value: float

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("Gamma span end must be >= start")
        if not math.isfinite(float(self.value)):
            raise ValueError("Gamma value must be finite")


@dataclass(frozen=True)
class GammaSchedule:
    """Ordered, non-overlapping piecewise Gamma schedule."""

    spans: tuple[GammaSpan, ...]

    def __post_init__(self) -> None:
        if not self.spans:
            raise ValueError("At least one Gamma span is required")
        ordered = tuple(sorted(self.spans, key=lambda s: s.start))
        if ordered != self.spans:
            raise ValueError("Gamma spans must be ordered by start year")
        for left, right in zip(self.spans, self.spans[1:]):
            if right.start <= left.end:
                raise ValueError("Gamma spans must not overlap")
            if right.start != left.end + 1:
                raise ValueError("Gamma spans must be contiguous")

    @classmethod
    def single(cls, start: int, end: int, value: float) -> "GammaSchedule":
        return cls((GammaSpan(start, end, float(value)),))

    def for_period(self, period: int) -> float:
        for span in self.spans:
            if span.start <= period <= span.end:
                return float(span.value)
        raise KeyError(
            f"No Gamma value configured for transition year {period}"
        )

    def values_for(self, periods: list[int] | tuple[int, ...]) -> list[float]:
        return [self.for_period(int(period)) for period in periods]

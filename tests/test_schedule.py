import pytest
from capital_analysis.domain.schedule import GammaSchedule, GammaSpan


def test_schedule_resolves_transition_year():
    schedule = GammaSchedule(
        (GammaSpan(1968, 1981, 1.0), GammaSpan(1982, 1991, 0.5))
    )
    assert schedule.for_period(1968) == 1.0
    assert schedule.for_period(1981) == 1.0
    assert schedule.for_period(1982) == 0.5


def test_schedule_requires_contiguous_spans():
    with pytest.raises(ValueError):
        GammaSchedule((GammaSpan(1968, 1981, 1.0), GammaSpan(1983, 1991, 0.5)))

"""Capital acquisition and retirement analysis."""

from .domain.acquisition import AcquisitionResult, calculate_acquisition
from .domain.models import CapitalDataset
from .domain.retirement import RetirementResult, calculate_retirement
from .domain.schedule import GammaSchedule, GammaSpan

__all__ = [
    "AcquisitionResult",
    "CapitalDataset",
    "GammaSchedule",
    "GammaSpan",
    "RetirementResult",
    "calculate_acquisition",
    "calculate_retirement",
]

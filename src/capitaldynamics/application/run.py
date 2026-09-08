from pathlib import Path

from ..data.csv import load_table
from ..domain.acquisition import AcquisitionResult, calculate_acquisition
from ..domain.retirement import RetirementResult, calculate_retirement
from .scenario import Scenario


def run_acquisition(
    input_path: str | Path, scenario_path: str | Path
) -> AcquisitionResult:
    dataset = load_table(input_path)
    scenario = Scenario.from_yaml(scenario_path)
    return calculate_acquisition(
        dataset, scenario.analysis_start, scenario.gamma
    )


def run_retirement(
    input_path: str | Path, scenario_path: str | Path
) -> RetirementResult:
    dataset = load_table(input_path)
    scenario = Scenario.from_yaml(scenario_path)
    return calculate_retirement(
        dataset, scenario.analysis_start, scenario.gamma
    )

from pathlib import Path

from capitaldynamics.analysis.acquisition import analyze_capital_acquisition
from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.config.paths import WAREHOUSE
from capitaldynamics.data.loader import load_data
from capitaldynamics.preparation.datasets import prepare_acquisition_data
from capitaldynamics.visualization.acquisition import (
    create_acquisition_figures,
)
from capitaldynamics.workflow.common import RunArtifacts, persist_run


def run_acquisition_analysis(
    gamma_schedule: GammaSchedule,
    *,
    warehouse: Path = WAREHOUSE,
    output_dir: Path | None = None,
    relation: str = "marts.capital_dynamics_archived",
    show: bool = False,
) -> RunArtifacts:
    """
    Run the full acquisition use case from DuckDB observations to artifacts.
    """
    raw = load_data(warehouse=warehouse, relation=relation)
    prepared = prepare_acquisition_data(raw)
    result = analyze_capital_acquisition(prepared, gamma_schedule)
    figures = create_acquisition_figures(
        prepared.frame,
        result,
        deflator_base_year=prepared.deflator_base_year,
    )
    metadata = {
        "warehouse": str(Path(warehouse).expanduser().resolve()),
        "source_relation": relation,
        "deflator_base_year": prepared.deflator_base_year,
        "gamma_schedule": gamma_schedule.as_records(
            int(result["year"].iloc[-1])
        ),
        "formula_version": "current-python-acquisition-v1",
    }
    return persist_run(
        analysis_name="acquisition",
        result=result,
        figures=figures,
        metadata=metadata,
        output_dir=output_dir,
        show=show,
    )

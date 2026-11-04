from pathlib import Path

from capitaldynamics.analysis.retirement import analyze_capital_retirement
from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.config.paths import WAREHOUSE
from capitaldynamics.data.loader import load_data
from capitaldynamics.preparation.datasets import prepare_retirement_data
from capitaldynamics.visualization.retirement import create_retirement_figures
from capitaldynamics.workflow.common import RunArtifacts, persist_run


def run_retirement_analysis(
    gamma_schedule: GammaSchedule,
    *,
    warehouse: Path = WAREHOUSE,
    output_dir: Path | None = None,
    relation: str = "marts.capital_dynamics_archived",
    start_year: int | None = None,
    show: bool = False,
) -> RunArtifacts:
    """
    Run the full retirement use case from DuckDB observations to artifacts.
    """
    raw = load_data(warehouse=warehouse, relation=relation)
    prepared = prepare_retirement_data(raw, start_year=start_year)
    result = analyze_capital_retirement(prepared, gamma_schedule)
    figures = create_retirement_figures(
        prepared.frame,
        result,
        deflator_base_year=prepared.deflator_base_year,
    )
    metadata = {
        "warehouse": str(Path(warehouse).expanduser().resolve()),
        "source_relation": relation,
        "deflator_base_year": prepared.deflator_base_year,
        "analysis_start_year": int(result["year"].iloc[0]),
        "gamma_schedule": gamma_schedule.as_records(
            int(result["year"].iloc[-1])
        ),
        "formula_version": "current-python-retirement-v1",
    }
    return persist_run(
        analysis_name="retirement",
        result=result,
        figures=figures,
        metadata=metadata,
        output_dir=output_dir,
        show=show,
    )

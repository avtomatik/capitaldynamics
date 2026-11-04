import json

import duckdb
import pandas as pd
import pytest

from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.data.loader import load_data
from capitaldynamics.workflow.acquisition import run_acquisition_analysis


def make_warehouse(path) -> None:
    with duckdb.connect(str(path)) as connection:
        connection.execute("CREATE SCHEMA marts")
        connection.execute(
            """
            CREATE TABLE marts.capital_dynamics_archived (
                year INTEGER,
                real_investment DOUBLE,
                nominal_gdp DOUBLE,
                real_gdp DOUBLE,
                full_capacity_real_gdp DOUBLE,
                real_fixed_assets DOUBLE,
                manufacturing_labor DOUBLE
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO marts.capital_dynamics_archived
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (2000, 10.0, 100.0, 100.0, 110.0, 50.0, 20.0),
                (2001, 11.0, 110.0, 105.0, 116.0, 53.0, 21.0),
                (2002, 12.0, 120.0, 110.0, 122.0, 55.0, 22.0),
                (2003, 13.0, 130.0, 115.0, 128.0, 58.0, 23.0),
            ],
        )


def test_loader_reads_sorted_semantic_relation_read_only(tmp_path) -> None:
    warehouse = tmp_path / "observations.duckdb"
    make_warehouse(warehouse)
    frame = load_data(warehouse)
    assert frame.index.name == "year"
    assert frame.index.tolist() == [2000, 2001, 2002, 2003]
    assert "real_investment" in frame.columns
    with duckdb.connect(str(warehouse), read_only=True) as connection:
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM marts.capital_dynamics_archived"
            ).fetchone()[0]
            == 4
        )


def test_loader_rejects_unsafe_relation_name(tmp_path) -> None:
    warehouse = tmp_path / "observations.duckdb"
    make_warehouse(warehouse)
    with pytest.raises(ValueError, match="schema-qualified"):
        load_data(
            warehouse,
            relation="marts.x; DROP TABLE marts.capital_dynamics_archived",
        )


def test_acquisition_workflow_publishes_complete_run(tmp_path) -> None:
    warehouse = tmp_path / "observations.duckdb"
    make_warehouse(warehouse)
    output_dir = tmp_path / "output" / "acquisition-run"
    artifacts = run_acquisition_analysis(
        GammaSchedule.from_pairs([(2000, 0.5)]),
        warehouse=warehouse,
        output_dir=output_dir,
    )
    assert artifacts.row_count == 4
    assert artifacts.results_csv.is_file()
    assert artifacts.manifest.is_file()
    assert len(artifacts.figures) == 5
    assert all(path.is_file() for path in artifacts.figures)
    result = pd.read_csv(artifacts.results_csv)
    assert result["year"].tolist() == [2000, 2001, 2002, 2003]
    manifest = json.loads(artifacts.manifest.read_text(encoding="utf-8"))
    assert manifest["analysis"] == "acquisition"
    assert manifest["gamma_schedule"][0]["start_year"] == 2000
    with pytest.raises(FileExistsError, match="never overwritten"):
        run_acquisition_analysis(
            GammaSchedule.from_pairs([(2000, 0.5)]),
            warehouse=warehouse,
            output_dir=output_dir,
        )

from pathlib import Path
from typing import Any

import duckdb

from capitaldynamics.config.paths import WAREHOUSE

###############################################################################
# Mart definitions
###############################################################################
#
# `series`
#     Source series required from raw.observations.
#
# `derived`
#     Columns calculated from the pivoted source series.
#
# `columns`
#     Columns exposed by the mart, in the desired order.
#
# `required`
#     Exposed columns that must be non-null for a row to survive.
#
# `workbooks`
#     Historical provenance/documentation. These are not read when rebuilding
#     the mart because the source observations are now in raw.observations.
#
###############################################################################


MART_DEFINITIONS: dict[str, dict[str, Any]] = {
    # =========================================================================
    # Historical workbook reconstruction 1
    # =========================================================================
    "dataset_1": {
        "workbooks": ["Calculation 2013-05-22-3 Revisited 2017-08-11.xlsm"],
        "series": ["A191RC1", "A191RX1", "A006RC1", "K160021", "A4601C0"],
        "required": ["A191RC1", "A191RX1", "A006RC1", "K160021", "A4601C0"],
    },
    # =========================================================================
    # Historical workbook reconstruction 2
    # =========================================================================
    "dataset_2": {
        "workbooks": [
            "Calculation 2013-07-09-1 Revisited 2017-08-14.xlsm",
            "Calculation 2013-07-09-2 Revisited 2017-08-14.xlsm",
            "Calculation 2013-07-09-3 Revisited 2017-08-14.xlsm",
            "Calculation 2013-07-09-4 Revisited 2017-08-14.xlsm",
        ],
        "series": [
            "A191RC1",
            "A191RX1",
            "A006RC1",
            "K160491",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "CAPUTL.B50001.A",
        ],
        "derived": {
            "bea_labor_mfg": """
                list_avg(
                    list_filter(
                        [
                            H4313C0,
                            J4313C0,
                            A4313C0,
                            N4313C0
                        ],
                        x -> x IS NOT NULL
                    )
                )
            """,
        },
    },
    # =========================================================================
    # Historical workbook reconstruction 3
    # =========================================================================
    "dataset_3": {
        "workbooks": ["Calculation 2013-08-18 Revisited 2017-09-04.xlsm"],
        "series": [
            "A191RC1",
            "A191RX1",
            "k3n31gd1es000",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "A032RC1",
            "CAPUTL.B50001.A",
        ],
    },
    # =========================================================================
    # Historical workbook reconstruction 4
    # =========================================================================
    "dataset_4": {
        "workbooks": [
            "Calculation 2013-09-23-1 Revisited 2017-09-01.xlsm",
            "Calculation 2013-09-23-2 Revisited 2017-09-01.xlsm",
            "Calculation 2013-09-23-3 Revisited 2017-09-01.xlsm",
            "Calculation 2013-09-23-4 Revisited 2017-09-01.xlsm",
        ],
        "series": [
            "A191RC1",
            "A191RX1",
            "K160491",
            "k3n31gd1es000",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "A032RC1",
            "CAPUTL.B50001.A",
        ],
    },
    # =========================================================================
    # Former LOCAL_DATASET
    # =========================================================================
    "local_dataset": {
        "series": [
            "A191RC1",
            "A191RX1",
            "k3n31gd1es000",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "A032RC1",
            "CAPUTL.B50001.A",
        ],
        "columns": [
            "A191RC1",
            "A191RX1",
            "k3n31gd1es000",
            "bea_labor_mfg",
            "A032RC1",
            "CAPUTL.B50001.A",
            "full_capacity_real_gdp",
        ],
        "derived": {
            "bea_labor_mfg": """
                list_avg(
                    list_filter(
                        [
                            H4313C0,
                            J4313C0,
                            A4313C0,
                            N4313C0
                        ],
                        x -> x IS NOT NULL
                    )
                )
            """,
            "full_capacity_real_gdp": """
                A191RX1
                / NULLIF("CAPUTL.B50001.A", 0)
            """,
        },
    },
    # =========================================================================
    # Historical reconstruction used by capital-dynamics analysis
    # =========================================================================
    #
    # This replaces the old combine_capital_combined_archived().
    #
    # H/J/A/N4313C0 are source inputs to the row-wise manufacturing-labor
    # average. They are therefore deliberately NOT required individually.
    #
    "capital_output_labor_archived": {
        "workbooks": ["Calculation 2013-05-22-3 Revisited 2017-08-11.xlsm"],
        "series": [
            "A006RC1",
            "A191RC1",
            "A191RX1",
            "K160021",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "CAPUTL.B50001.A",
            "A4601C0",
        ],
        "columns": [
            "A006RC1",
            "A191RC1",
            "A191RX1",
            "K160021",
            "CAPUTL.B50001.A",
            "bea_labor_mfg",
            "A4601C0",
        ],
        "derived": {
            "bea_labor_mfg": """
                list_avg(
                    list_filter(
                        [
                            H4313C0,
                            J4313C0,
                            A4313C0,
                            N4313C0
                        ],
                        x -> x IS NOT NULL
                    )
                )
            """,
        },
        "required": [
            "A006RC1",
            "A191RC1",
            "A191RX1",
            "K160021",
            "CAPUTL.B50001.A",
            "bea_labor_mfg",
            "A4601C0",
        ],
    },
}


###############################################################################
# SQL helpers
###############################################################################
def sql_identifier(name: str) -> str:
    """Quote a SQL identifier for DuckDB."""
    return '"' + name.replace('"', '""') + '"'


def sql_string_literal(value: str) -> str:
    """Quote a SQL string literal for DuckDB."""
    return "'" + value.replace("'", "''") + "'"


def sql_string_list(values: list[str]) -> str:
    """Render a list of Python strings as SQL string literals."""
    return ",\n".join(sql_string_literal(value) for value in values)


def pivot_sql(series: list[str]) -> str:
    """
    Return the common raw.observations -> wide-table PIVOT expression.
    The explicit IN list keeps the resulting column set deterministic.
    """
    values = sql_string_list(series)
    return f"""
        PIVOT raw.observations
        ON series_code IN (
            {values}
        )
        USING FIRST(value)
        GROUP BY year
    """


###############################################################################
# Validation
###############################################################################
def _duplicates(values: list[str]) -> list[str]:
    """Return duplicated values in deterministic order."""
    return sorted({value for value in values if values.count(value) > 1})


def validate_mart_definition(name: str, definition: dict[str, Any]) -> None:
    """Validate one mart definition."""
    if not isinstance(name, str) or not name:
        raise ValueError("Mart name must be a non-empty string.")
    series = definition.get("series")
    if not isinstance(series, list) or not series:
        raise ValueError(
            f"Mart {name!r} must define a non-empty `series` list."
        )
    invalid_series = [
        value for value in series if not isinstance(value, str) or not value
    ]
    if invalid_series:
        raise ValueError(
            f"Mart {name!r} contains invalid series codes: "
            f"{invalid_series!r}."
        )
    duplicate_series = _duplicates(series)
    if duplicate_series:
        raise ValueError(
            f"Mart {name!r} contains duplicate source series: "
            f"{duplicate_series!r}."
        )
    derived = definition.get("derived", {})
    if not isinstance(derived, dict):
        raise ValueError(
            f"Mart {name!r} must define `derived` as a dictionary."
        )
    overlapping = sorted(set(series) & set(derived))
    if overlapping:
        raise ValueError(
            f"Mart {name!r} defines these names both as source and derived "
            f"columns: {overlapping!r}."
        )
    for column_name, expression in derived.items():
        if not isinstance(column_name, str) or not column_name:
            raise ValueError(
                f"Mart {name!r} contains an invalid derived column name."
            )
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError(
                f"Mart {name!r} has an empty expression for "
                f"{column_name!r}."
            )
        if ";" in expression:
            raise ValueError(
                f"Mart {name!r}, derived column {column_name!r}, "
                "contains ';'. Multiple SQL statements are not allowed."
            )
    available_columns = set(series) | set(derived)
    columns = definition.get("columns", [*series, *derived])
    if not isinstance(columns, list):
        raise ValueError(f"Mart {name!r} must define `columns` as a list.")
    duplicate_columns = _duplicates(columns)
    if duplicate_columns:
        raise ValueError(
            f"Mart {name!r} exposes duplicate columns: "
            f"{duplicate_columns!r}."
        )
    unknown_columns = sorted(set(columns) - available_columns)
    if unknown_columns:
        raise ValueError(
            f"Mart {name!r} exposes unknown columns: " f"{unknown_columns!r}."
        )
    required = definition.get("required", [])
    if not isinstance(required, list):
        raise ValueError(f"Mart {name!r} must define `required` as a list.")
    duplicate_required = _duplicates(required)
    if duplicate_required:
        raise ValueError(
            f"Mart {name!r} contains duplicate required columns: "
            f"{duplicate_required!r}."
        )
    unknown_required = sorted(set(required) - set(columns))
    if unknown_required:
        raise ValueError(
            f"Mart {name!r} requires columns that are not exposed: "
            f"{unknown_required!r}."
        )


def validate_mart_definitions(definitions: dict[str, dict[str, Any]]) -> None:
    """Validate the complete mart configuration."""
    if not definitions:
        raise ValueError("No mart definitions configured.")
    duplicate_names = _duplicates(list(definitions))
    if duplicate_names:
        raise ValueError(f"Duplicate mart names: {duplicate_names!r}.")
    for name, definition in definitions.items():
        validate_mart_definition(name, definition)


def _requested_series(definitions: dict[str, dict[str, Any]]) -> list[str]:
    """Return all unique source series required by all configured marts."""
    return sorted(
        {
            series_code
            for definition in definitions.values()
            for series_code in definition["series"]
        }
    )


def validate_raw_observations(
    con: duckdb.DuckDBPyConnection, definitions: dict[str, dict[str, Any]]
) -> None:
    """
    Validate the raw observation table required by all marts.
    Expected relation:
        raw.observations(
            year,
            series_code,
            value
        )
    Expected key:
        (year, series_code)
    must identify at most one observation.
    """
    try:
        con.execute(
            """
            SELECT
                year,
                series_code,
                value
            FROM raw.observations
            LIMIT 0
            """
        )
    except Exception as exc:
        raise RuntimeError(
            "The required relation raw.observations is not available "
            "with columns year, series_code, value."
        ) from exc
    requested = _requested_series(definitions)
    requested_sql = sql_string_list(requested)
    missing = con.execute(
        f"""
        SELECT
            requested.series_code
        FROM (
            SELECT
                series_code
            FROM (
                VALUES
                    {", ".join(f"({sql_string_literal(s)})" for s in requested)}
            ) AS t(series_code)
        ) AS requested
        LEFT JOIN (
            SELECT DISTINCT series_code
            FROM raw.observations
            WHERE series_code IN ({requested_sql})
        ) AS observed
            USING (series_code)
        WHERE observed.series_code IS NULL
        ORDER BY requested.series_code
        """
    ).fetchall()
    if missing:
        raise ValueError(
            "raw.observations is missing configured source series: "
            f"{[row[0] for row in missing]!r}."
        )
    duplicate = con.execute(
        f"""
        SELECT
            year,
            series_code,
            COUNT(*) AS row_count
        FROM raw.observations
        WHERE series_code IN ({requested_sql})
        GROUP BY
            year,
            series_code
        HAVING COUNT(*) > 1
        ORDER BY
            year,
            series_code
        LIMIT 1
        """
    ).fetchone()
    if duplicate is not None:
        year, series_code, row_count = duplicate
        raise ValueError(
            "raw.observations violates the expected uniqueness contract: "
            f"(year={year!r}, series_code={series_code!r}) occurs "
            f"{row_count} times."
        )
    null_year_count = con.execute(
        f"""
        SELECT COUNT(*)
        FROM raw.observations
        WHERE series_code IN ({requested_sql})
          AND year IS NULL
        """
    ).fetchone()[0]
    if null_year_count:
        raise ValueError(
            "raw.observations contains "
            f"{null_year_count} requested observations with NULL year."
        )


###############################################################################
# Mart SQL compilation
###############################################################################
def _derived_ctes(
    base_relation: str, derived: dict[str, str]
) -> tuple[list[str], str]:
    """
    Compile derived columns into sequential CTEs.
    Sequential CTEs intentionally permit one derived column to refer to a
    derived column defined earlier in the same definition.
    """
    ctes: list[str] = []
    current_relation = base_relation
    for position, (column_name, expression) in enumerate(derived.items()):
        next_relation = f"derived_{position}"
        ctes.append(
            f"""
            {next_relation} AS (
                SELECT
                    *,
                    {expression.strip()} AS {sql_identifier(column_name)}
                FROM {current_relation}
            )
            """
        )
        current_relation = next_relation
    return ctes, current_relation


def compile_mart_sql(name: str, definition: dict[str, Any]) -> str:
    """Compile a validated mart definition into CREATE VIEW SQL."""
    validate_mart_definition(name, definition)
    series = definition["series"]
    derived = definition.get("derived", {})
    columns = definition.get("columns", [*series, *derived])
    required = definition.get("required", [])
    ctes = [
        f"""
        pivoted AS (
            {pivot_sql(series)}
        )
        """
    ]
    derived_ctes, final_relation = _derived_ctes("pivoted", derived)
    ctes.extend(derived_ctes)
    output_columns = ",\n            ".join(
        sql_identifier(column_name) for column_name in columns
    )
    where_clause = ""
    if required:
        predicates = [
            f"{sql_identifier(column_name)} IS NOT NULL"
            for column_name in required
        ]
        where_clause = "WHERE " + "\n              AND ".join(predicates)
    return f"""
        CREATE OR REPLACE VIEW
            marts.{sql_identifier(name)}
        AS
        WITH
        {", ".join(ctes)}
        SELECT
            year,
            {output_columns}
        FROM {final_relation}
        {where_clause}
        ORDER BY year
    """


def create_mart(
    con: duckdb.DuckDBPyConnection, name: str, definition: dict[str, Any]
) -> None:
    """Create or replace one source/reconstruction mart view."""
    con.execute(compile_mart_sql(name, definition))


###############################################################################
# Semantic analysis views
###############################################################################
def create_capital_dynamics_archived(con: duckdb.DuckDBPyConnection) -> None:
    """
    Create the semantic dataset consumed by the archived capital-dynamics code.
    The upstream mart retains historical source identifiers. This view
    translates those identifiers into stable economic names and performs the
    derived calculations formerly done in pandas.
    Capacity utilization is deliberately an internal calculation input and is
    NOT exposed by this view.
    """
    con.execute(
        """
        CREATE OR REPLACE VIEW
            marts.capital_dynamics_archived
        AS
        SELECT
            year,
            -------------------------------------------------------------------
            -- Nominal investment
            -------------------------------------------------------------------
            A006RC1
                AS nominal_investment,
            -------------------------------------------------------------------
            -- Output
            -------------------------------------------------------------------
            A191RC1
                AS nominal_gdp,
            A191RX1
                AS real_gdp,
            -------------------------------------------------------------------
            -- Investment expressed in real-GDP terms
            -------------------------------------------------------------------
            A006RC1
                * A191RX1
                / NULLIF(A191RC1, 0)
                AS real_investment,
            -------------------------------------------------------------------
            -- GDP at full capacity
            -------------------------------------------------------------------
            A191RC1
                / NULLIF("CAPUTL.B50001.A", 0)
                AS full_capacity_nominal_gdp,
            A191RX1
                / NULLIF("CAPUTL.B50001.A", 0)
                AS full_capacity_real_gdp,
            -------------------------------------------------------------------
            -- Fixed assets expressed in real-output terms
            -------------------------------------------------------------------
            K160021
                * A191RX1
                / NULLIF(A191RC1, 0)
                AS real_fixed_assets,
            -------------------------------------------------------------------
            -- Manufacturing labor
            -------------------------------------------------------------------
            bea_labor_mfg
                AS manufacturing_labor
        FROM marts.capital_output_labor_archived
        ORDER BY year
        """
    )


###############################################################################
# Build all marts
###############################################################################
def build_marts(warehouse: Path = WAREHOUSE) -> None:
    """
    Validate and build all historical reconstruction and semantic views.
    The build is transactional: either all views are created successfully or
    the transaction is rolled back.
    """
    validate_mart_definitions(MART_DEFINITIONS)
    warehouse.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(warehouse)) as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS marts")
        validate_raw_observations(con, MART_DEFINITIONS)
        con.execute("BEGIN")
        try:
            for name, definition in MART_DEFINITIONS.items():
                create_mart(con, name, definition)
            # Semantic layer built on top of the historical reconstruction.
            create_capital_dynamics_archived(con)
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise


###############################################################################
# Exploration / verification
###############################################################################
def print_marts(warehouse: Path = WAREHOUSE) -> None:
    """Print every reconstructed and semantic mart."""
    with duckdb.connect(str(warehouse), read_only=True) as con:
        mart_names = [*MART_DEFINITIONS, "capital_dynamics_archived"]
        for name in mart_names:
            print(f"\n{'=' * 80}")
            print(f"marts.{name}")
            print(f"{'=' * 80}")
            con.sql(
                f"""
                SELECT *
                FROM marts.{sql_identifier(name)}
                ORDER BY year
                """
            ).show()


###############################################################################
# Script entry point
###############################################################################
if __name__ == "__main__":
    build_marts()
    print_marts()

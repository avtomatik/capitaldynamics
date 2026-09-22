from pathlib import Path

import duckdb

from .paths import WAREHOUSE

###############################################################################
# Mart definitions
###############################################################################
# Each entry records which historical workbook(s) produced the mart and which
# source series are required to reconstruct it.
# The order of `series` is also the order used in the resulting view.
###############################################################################
MARTS = {
    "dataset_1": {
        "workbooks": [
            "Calculation 2013-05-22-3 Revisited 2017-08-11.xlsm",
        ],
        "series": [
            "A191RC1",
            "A191RX1",
            "A006RC1",
            "K160021",
            "A4601C0",
        ],
        "drop_incomplete": True,
    },
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
            """CAPUTL.B50001.A""",
        ],
        "drop_incomplete": False,
        "derived": {
            "bea_labor_mfg": """
                list_avg(
                    list_filter(
                        [H4313C0, J4313C0, A4313C0, N4313C0],
                        x -> x IS NOT NULL
                    )
                )
            """,
        },
    },
    "dataset_3": {
        "workbooks": [
            "Calculation 2013-08-18 Revisited 2017-09-04.xlsm",
        ],
        "series": [
            "A191RC1",
            "A191RX1",
            "k3n31gd1es000",
            "H4313C0",
            "J4313C0",
            "A4313C0",
            "N4313C0",
            "A032RC1",
            """CAPUTL.B50001.A""",
        ],
        "drop_incomplete": False,
    },
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
            """CAPUTL.B50001.A""",
        ],
        "drop_incomplete": False,
    },
}


###############################################################################
# SQL generation
###############################################################################
def sql_string_list(values: list[str]) -> str:
    return ",\n".join(f"'{value}'" for value in values)


def pivot_sql(series: list[str]) -> str:
    """Return a static DuckDB PIVOT expression for the requested series."""
    values = sql_string_list(series)
    return f"""
        PIVOT raw.observations
        ON series_code IN (
            {values}
        )
        USING FIRST(value)
        GROUP BY year
    """


def sql_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def create_mart(
    con: duckdb.DuckDBPyConnection, name: str, definition: dict
) -> None:
    series = definition["series"]
    select_columns = [
        "year",
        *(sql_identifier(s) for s in series),
    ]
    for column_name, expression in definition.get("derived", {}).items():
        select_columns.append(
            f"{expression.strip()} AS {sql_identifier(column_name)}"
        )
    select_sql = ",\n            ".join(select_columns)
    pivot = pivot_sql(series)
    where_clause = ""
    if definition.get("drop_incomplete"):
        required_columns = "\n          AND ".join(
            f"{sql_identifier(series_code)} IS NOT NULL"
            for series_code in series
        )
        where_clause = f"""
        WHERE {required_columns}
        """
    sql = f"""
        CREATE OR REPLACE VIEW marts.{name} AS
        SELECT
            {select_sql}
        FROM (
            {pivot}
        )
        {where_clause}
        """
    con.execute(sql)


###############################################################################
# Build all marts
###############################################################################
def build_marts(warehouse: Path = WAREHOUSE) -> None:
    """Build all historical data-archeology marts."""
    warehouse.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(warehouse)) as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS marts")
        for name, definition in MARTS.items():
            create_mart(con, name, definition)


###############################################################################
# Exploration / verification
###############################################################################
def print_marts(warehouse: Path = WAREHOUSE) -> None:
    """Print every mart for quick inspection."""
    with duckdb.connect(str(warehouse), read_only=True) as con:
        for name in MARTS:
            print(f"\n{'=' * 80}")
            print(f"marts.{name}")
            print(f"{'=' * 80}")
            df = con.sql(
                f"""
                SELECT *
                FROM marts.{name}
                ORDER BY year
                """
            ).df()
            print(df)


if __name__ == "__main__":
    build_marts()
    print_marts()

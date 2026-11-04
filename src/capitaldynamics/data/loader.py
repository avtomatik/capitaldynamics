import re
from pathlib import Path

import duckdb
import pandas as pd

from capitaldynamics.config.paths import WAREHOUSE

_RELATION_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*$")


def load_data(
    warehouse: Path = WAREHOUSE,
    relation: str = "marts.capital_dynamics_archived",
) -> pd.DataFrame:
    """Load the semantic capital-dynamics dataset from DuckDB.
    The connection is read-only. Relation names are validated before being
    interpolated because SQL identifiers cannot be bound as query parameters.
    The returned frame is ordered by year and has ``year`` as its index.
    """
    warehouse = Path(warehouse)
    if not warehouse.is_file():
        raise FileNotFoundError(
            f"DuckDB warehouse does not exist: {warehouse}. "
            "Run the existing ingestion and mart-building steps first."
        )
    if not _RELATION_RE.fullmatch(relation):
        raise ValueError(
            "relation must be a schema-qualified SQL identifier, "
            "for example 'marts.capital_dynamics_archived'."
        )
    schema, name = relation.split(".", maxsplit=1)
    quoted_relation = f'"{schema}"."{name}"'
    query = f"SELECT * FROM {quoted_relation} ORDER BY year"
    try:
        with duckdb.connect(str(warehouse), read_only=True) as connection:
            frame = connection.execute(query).fetchdf()
    except duckdb.Error as exc:
        raise RuntimeError(
            f"Could not read {relation!r} from DuckDB warehouse {warehouse}. "
            "Confirm that the mart has been built and is readable."
        ) from exc
    if frame.empty:
        raise ValueError(
            f"The warehouse relation {relation!r} contains no rows."
        )
    if "year" not in frame.columns:
        raise ValueError(
            f"The warehouse relation {relation!r} has no 'year' column."
        )
    if frame["year"].duplicated().any():
        duplicates = frame.loc[frame["year"].duplicated(), "year"].tolist()
        raise ValueError(
            f"The warehouse relation {relation!r} contains duplicate years: "
            f"{duplicates[:10]!r}."
        )
    return frame.set_index("year").sort_index()

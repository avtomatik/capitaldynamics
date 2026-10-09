import duckdb
import pandas as pd

from capitaldynamics.config.paths import WAREHOUSE


def load_data() -> pd.DataFrame:
    query = """
    SELECT *
    FROM marts.capital_dynamics_archived
    ORDER BY year
    """
    with duckdb.connect(str(WAREHOUSE), read_only=True) as connection:
        return connection.execute(query).fetchdf().set_index("year")

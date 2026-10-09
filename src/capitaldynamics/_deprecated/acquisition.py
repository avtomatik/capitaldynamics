import duckdb

from capitaldynamics._deprecated.visualization import plot_capital_acquisition
from capitaldynamics.config.paths import WAREHOUSE

with duckdb.connect(str(WAREHOUSE), read_only=True) as con:
    df = con.sql(
        """
        SELECT *
        FROM marts.capital_dynamics_archived
        ORDER BY year
        """
    ).df()

    df = df.set_index("year")

    df.loc[
        :,
        [
            "real_investment",
            "real_gdp",
            "nominal_gdp",
            "full_capacity_real_gdp",
            "real_fixed_assets",
            "manufacturing_labor",
        ],
    ].pipe(plot_capital_acquisition)

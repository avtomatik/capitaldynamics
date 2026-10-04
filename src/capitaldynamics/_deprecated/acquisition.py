import duckdb

from capitaldynamics._deprecated.paths import WAREHOUSE
from capitaldynamics._deprecated.visualization import plot_capital_acquisition

###############################################################################
# BASE_YEAR = 1967
###############################################################################
with duckdb.connect(str(WAREHOUSE), read_only=True) as con:
    # df = con.sql(
    #     """
    #     SELECT *
    #     FROM marts.local_dataset
    #     ORDER BY year
    #     """
    # ).df()
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

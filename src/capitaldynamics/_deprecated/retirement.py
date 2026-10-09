import duckdb

from capitaldynamics._deprecated.visualization import plot_capital_retirement
from capitaldynamics._retired.visualization import run_capital_retirement
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
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(plot_capital_retirement)

df.loc[
    :,
    [
        "real_investment",
        "real_gdp",
        "nominal_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(run_capital_retirement)

df.loc[
    :,
    [
        "real_investment",
        "full_capacity_real_gdp",
        "nominal_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(plot_capital_retirement)

df.loc[
    :,
    [
        "real_investment",
        "full_capacity_real_gdp",
        "nominal_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(run_capital_retirement)

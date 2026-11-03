from capitaldynamics.data.loader import load_data

from .visualization import analyze_capital_productivity

COLUMNS = [
    "real_investment",
    "nominal_gdp",
    "real_gdp",
    "full_capacity_real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
]


def main() -> None:
    data = load_data()
    data.loc[:, COLUMNS].pipe(analyze_capital_productivity)


if __name__ == "__main__":
    main()

"""Identifiers and URLs recovered from the original research project."""

BEA_NIPA_URL = "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"
BEA_FIXED_ASSETS_URL = (
    "https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt"
)
FED_CAPACITY_UTILIZATION_SERIES = "CAPUTL.B50001.A"

ORIGINAL_SERIES = {
    "nominal_investment": "A006RC",
    "nominal_gdp": "A191RC",
    "real_gdp": "A191RX",
    "nominal_capital": "k1n31gd1es00",
    "labor_overall": "A4601C",
    "capacity_utilization": FED_CAPACITY_UTILIZATION_SERIES,
}

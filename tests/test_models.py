import pandas as pd
from capital_analysis.domain.models import CapitalDataset


def sample_frame():
    return pd.DataFrame(
        {
            "period": [2004, 2005, 2006],
            "nominal_gdp": [90.0, 100.0, 110.0],
            "real_gdp": [90.0, 100.0, 110.0],
            "nominal_investment": [10.0, 11.0, 12.0],
            "nominal_capital": [50.0, 55.0, 60.0],
            "labor": [10.0, 10.0, 10.0],
            "capacity_utilization": [1.0, 1.0, 1.0],
        }
    )


def test_base_year_comes_from_nominal_real_match():
    data = CapitalDataset.from_frame(sample_frame())
    assert data.base_year() == 2004


def test_enriched_data_contains_real_series():
    data = CapitalDataset.from_frame(sample_frame())
    enriched = data.enriched()
    assert enriched.loc[1, "real_investment"] == 11.0
    assert enriched.loc[1, "real_capital"] == 55.0

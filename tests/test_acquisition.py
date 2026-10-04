import pandas as pd
from capital_analysis.domain.acquisition import calculate_acquisition
from capital_analysis.domain.models import CapitalDataset
from capital_analysis.domain.schedule import GammaSchedule


def test_acquisition_formula_matches_historical_vba():
    frame = pd.DataFrame(
        {
            "year": [2004, 2005, 2006],
            "nominal_gdp": [100.0, 100.0, 100.0],
            "real_gdp": [100.0, 100.0, 100.0],
            "nominal_investment": [10.0, 20.0, 30.0],
            "nominal_capital": [50.0, 60.0, 70.0],
            "labor": [10.0, 10.0, 10.0],
            "capacity_utilization": [1.0, 1.0, 1.0],
        }
    )
    result = calculate_acquisition(
        CapitalDataset.from_frame(frame),
        analysis_start=2004,
        gamma=GammaSchedule.single(2005, 2006, 2.0),
    )
    assert (
        result.data.loc[0, "capital_acquisition"]
        != result.data.loc[0, "capital_acquisition"]
    )
    assert result.data.loc[1, "capital_acquisition"] == 50.0

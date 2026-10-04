import pandas as pd

from capitaldynamics.domain.models import CapitalDataset
from capitaldynamics.domain.retirement import calculate_retirement
from capitaldynamics.domain.schedule import GammaSchedule


def test_retirement_formula_matches_historical_python():
    frame = pd.DataFrame(
        {
            "year": [2004, 2005, 2006],
            "nominal_gdp": [100.0, 100.0, 100.0],
            "real_gdp": [100.0, 100.0, 100.0],
            "nominal_investment": [10.0, 20.0, 30.0],
            "nominal_capital": [50.0, 60.0, 70.0],
            "labor": [10.0, 10.0, 10.0],
        }
    )
    result = calculate_retirement(
        CapitalDataset.from_frame(frame),
        analysis_start=2004,
        gamma=GammaSchedule.single(2004, 2005, 2.0),
    )
    assert result.data.loc[0, "retirement_value"] == 10.0
    assert result.data.loc[0, "retirement_ratio"] == 10.0 / 60.0

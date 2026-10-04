# Capital Analysis

A clean-room rewrite of the original `capital_interactive` research experiment. The project analyzes annual economic time series through two related models:

- **capital acquisition** — estimates gross capital formation / capital acquisition from changes in the capital stock and a piecewise Gamma conversion parameter;
- **capital retirement** — estimates fixed-asset retirement value and retirement ratio from changes in the capital stock and the same class of piecewise parameter.

The original project grew around two large interactive plotting functions. This rewrite deliberately moves the mathematics away from plotting, terminal input, and pandas positional indexing. The resulting model is deterministic, testable, and reusable from a CLI, notebook, or another Python program.

## Historical model recovered from the Excel/VBA experiment

The original spreadsheet computes a GDP deflator as:

`D_t = real_gdp_t / nominal_gdp_t`

and constructs:

`real_investment_t = nominal_investment_t * D_t`

`real_capital_t = nominal_capital_t * D_t`

The capacity-utilization-adjusted output used by the acquisition analysis is:

`maximum_output_t = real_gdp_t / capacity_utilization_t`

The acquisition estimate for transition `t -> t+1` is:

`acquisition_t = K_(t+1) - K_t + Gamma_t * I_(t+1)`

The retirement estimate is:

`retirement_value_t = K_t - K_(t+1) + Gamma_t * I_t`

`retirement_ratio_t = retirement_value_t / K_(t+1)`

The Excel experiment also normalizes indicators to a selected **analysis start year**. That is distinct from the GDP price-index **base year**. Both concepts are represented explicitly in the new model.

## Input data

The analysis accepts a canonical table containing:

| Column | Meaning |
|---|---|
| `year` | Year |
| `nominal_gdp` | Nominal GDP |
| `real_gdp` | Real GDP |
| `nominal_investment` | Gross private domestic investment |
| `nominal_capital` | Closing-balance fixed assets |
| `labor` | Labor series |
| `capacity_utilization` | FRS manufacturing capacity utilization |

Only `capacity_utilization` is required for the acquisition model.

A canonical CSV example is provided in `examples/capital_data.csv`.

## Scenarios

Model scenarios live in `configs/`. A scenario is explicit data rather than a sequence of `input()` calls:

```yaml
name: acquisition_4_spans
analysis_start: 1968
gamma:
  - {start: 1968, end: 1981, value: 1.0}
  - {start: 1982, end: 1991, value: 0.537711622818944}
  - {start: 1992, end: 2001, value: 0.815869779361117}
  - {start: 2002, end: 2010, value: 0.956084835528969}
```

The interval endpoints describe the **target year** on which the acquisition parameter is applied. Thus `1968..1981` means the transitions `1967 -> 1968` through `1980 -> 1981`; this matches the original VBA, whose output row is labeled by the target year. The retirement model uses the source-year convention described below.

## CLI

Install locally with uv or pip. Example with uv:

```bash
uv sync
uv run capital acquisition \
  --input examples/capital_data.csv \
  --config configs/example_acquisition.yaml \
  --output results/acquisition.csv

uv run capital retirement \
  --input examples/capital_data.csv \
  --config configs/example_retirement.yaml \
  --output results/retirement.csv
```

Add `--plot-dir results/plots --show` to create the corresponding figures.

## Python API

```python
import pandas as pd

from capital_analysis.domain.models import CapitalDataset
from capital_analysis.domain.schedule import GammaSchedule, GammaSpan
from capital_analysis.domain.acquisition import calculate_acquisition

raw = pd.read_csv("examples/capital_data.csv")
data = CapitalDataset.from_frame(raw)

schedule = GammaSchedule((
    GammaSpan(1968, 1981, 1.0),
    GammaSpan(1982, 1991, 0.537711622818944),
    GammaSpan(1992, 2001, 0.815869779361117),
    GammaSpan(2002, 2010, 0.956084835528969),
))

result = calculate_acquisition(data, analysis_start=1968, gamma=schedule)
print(result.table())
```

## Repository structure

```text
src/capital_analysis/
├── domain/          pure mathematical model and value objects
├── data/            input adapters and source metadata
├── application/    scenario orchestration
├── visualization/  plotting only
└── cli.py           thin command-line adapter
```

The `domain` package has no dependency on matplotlib and does not read from stdin.

## Tests

```bash
uv run pytest
```

## Data provenance

The original experiment used BEA NIPA data, BEA fixed-assets data, and Federal Reserve capacity-utilization data. Series identifiers from the original project are preserved in `src/capital_analysis/data/sources.py`. The rewrite intentionally separates those source identifiers from the analytical model.

## Historical scenarios

`configs/acquisition_4_spans.yaml` and the retirement scenarios reproduce the parameter schedules recovered from the original Excel experiment. They expect a source dataset covering the years named by the scenario. The checked-in example dataset is intentionally small and self-contained for smoke testing.

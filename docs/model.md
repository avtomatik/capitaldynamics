# Model notes

## Price deflator and real series

The recovered Excel procedure forms `D = real GDP / nominal GDP`, then uses `D` to convert nominal investment and nominal fixed assets into the model's real series.

## Analysis start vs price base

The price base year is identified from the year where nominal GDP and real GDP coincide in the original data. The analysis start is selected independently by the researcher. Normalized capital intensity, labor productivity, and investment/output indicators use the analysis start as their reference.

## Maximum output

The acquisition experiment constructs a capacity-adjusted maximum output as `real GDP / capacity utilization`. Ratios involving maximum output are normalized to the same analysis start.

## Gamma schedule

A Gamma span applies to named transition years. Acquisition follows the historical spreadsheet convention that the estimate for year `t` uses the transition from `t-1` to `t` and `Gamma_t`. Retirement uses the historical Python/Excel convention that the estimate labeled year `t` uses `K_t - K_(t+1) + Gamma_t * I_t`.

# Capital Dynamics

This is an **overlay/refactor pack** for the files supplied in the project description. It is not a full copy of the repository: the upstream collector and the existing `data/marts.py` implementation were not included in the supplied source. Those parts must remain in the repository and continue producing `raw.observations` and `marts.capital_dynamics_archived`.

The pack replaces the analysis entry points and adds explicit preparation, calculation, visualization, and run-persistence layers. It intentionally does not invent a replacement for the absent data-ingestion code.

## Design goals

- Read observations from DuckDB in read-only mode.
- Keep the existing raw-observation and mart-building boundary.
- Validate required columns, years, numeric values, finite values, and denominators before analysis.
- Keep model calculations deterministic and free of prompts, filesystem access, database access, and plotting.
- Keep visualization independent of data collection and model calculations.
- Require Gamma breakpoints explicitly; there are no hidden `input()` prompts.
- Write each run into a new directory containing `results.csv`, PNG charts, and `manifest.json`.
- Never overwrite an earlier run. Files are staged and the completed run directory is published with a same-filesystem rename.
- Return a non-zero exit status on invalid input or failed execution, so a scheduler can detect failures.

## Architecture

```text
capitaldynamics/
├── analysis/
│   ├── acquisition.py       # pure acquisition calculations
│   ├── retirement.py        # pure retirement calculations
│   └── segmentation.py      # validated piecewise Gamma schedule
├── config/
│   └── paths.py             # paths only; no directory creation on import
├── data/
│   └── loader.py            # read-only DuckDB adapter
├── preparation/
│   └── datasets.py          # source-data contracts and validation
├── visualization/
│   ├── common.py
│   ├── acquisition.py       # five acquisition figures
│   └── retirement.py        # seven retirement figures
├── workflow/
│   ├── common.py            # run artifacts and atomic publication
│   ├── acquisition.py       # acquisition use-case orchestration
│   └── retirement.py        # retirement use-case orchestration
├── cli.py                   # command-line interface
├── acquisition.py           # compatibility command entry point
├── retirement.py            # compatibility command entry point
└── __main__.py
```

The existing `capitaldynamics/data/marts.py` remains the mart compiler and definition registry. It is deliberately not replaced by this pack.

## Data contract

The semantic relation `marts.capital_dynamics_archived` must expose these columns:

| Column | Acquisition | Retirement |
|---|:---:|:---:|
| `year` | Yes | Yes |
| `real_investment` | Yes | Yes |
| `nominal_gdp` | Yes | Yes |
| `real_gdp` | Yes | Yes |
| `full_capacity_real_gdp` | Yes | No |
| `real_fixed_assets` | Yes | Yes |
| `manufacturing_labor` | Yes | Yes |

The relation must contain one row per year, in increasing year order, with at least two observations. Required numeric series must be finite. GDP, fixed assets, and labor must be positive. Initial real investment must be non-zero because the investment/output indices are normalised to the first analysis observation.

The deflator reference year is the latest year for which:

```text
abs(nominal_gdp - real_gdp) <= 1.0
```

This retains the historical absolute-difference convention. Unlike the old unbounded backwards loop, the preparation layer fails with a clear error if no such year exists.

## Gamma schedule semantics

Gamma values are supplied as **source-year breakpoints**. A value becomes active for the transition beginning in its specified year.

For example:

```text
--gamma 1947=0.90 --gamma 1970=1.05 --gamma 1995=0.98
```

means:

- Gamma 0.90 applies to transitions whose source year is 1947–1969.
- Gamma 1.05 applies to transitions whose source year is 1970–1994.
- Gamma 0.98 applies from source year 1995 to the final transition.

The first breakpoint must equal the first year included in the analysis. Every breakpoint must be an observed year with a following observation. Breakpoints must be strictly increasing. This removes the old ambiguity between worksheet row numbers, zero-based Python positions, and calendar years.

## Model equations and compatibility notes

### Acquisition

The static indicators retain the current Python implementation:

- `YAA`: observed output / real fixed assets.
- `YBB`: investment-to-output ratio, normalised to the first observation.
- `YCC`: labour capital intensity index.
- `YDD`: observed labour productivity index.
- `YEE`: log labour capital intensity index.
- `YFF`: log observed labour productivity index.
- `YGG`: full-capacity output / real fixed assets.
- `YHH`: full-capacity investment-to-output index.
- `YII`: full-capacity labour productivity index.
- `YJJ`: log full-capacity labour productivity index.

The dynamic estimate retains the current Python equation:

```text
estimate[t] = K[t] - K[t-1] + Gamma[source_year] * I[t]
```

The first observation has no preceding transition, so its estimate is null.

### Retirement

The static indicators retain the current Python implementation:

- `YAA`: log labour capital intensity index.
- `YBB`: log labour productivity index.
- `YCC`: investment-to-output index.
- `YDD`: fixed-assets turnover.
- `YEE`: estimated retirement value.
- `YFF`: estimated retirement value / end-period capital.
- `YGG`: absolute deviation of the retirement ratio from its sample mean.
- `YHH`: absolute period-to-period change in the retirement ratio.

The existing Python dynamic equation is retained explicitly:

```text
retirement_value[t+1] = K[t] - K[t+1] + Gamma[t] * I[t]
retirement_ratio[t+1] = retirement_value[t+1] / K[t+1]
```

**This is not equivalent to the legacy VBA retirement equation**, which uses `K[t+1] - K[t] + Gamma[t] * I[t+1]`. The legacy VBA retirement procedure also uses a user-selected starting year and calculates full-capacity output indicators that the current Python retirement workflow does not expose. The pack adds `--start-year` but does not silently change these model definitions.

Before treating the retirement output as a validated continuation of the historical workbook, the owner of the economic model should choose and document which equation is authoritative. The current equation is tagged as `current-python-retirement-v1` in the run manifest so outputs remain traceable.

## Installation and integration

1. Back up or commit the current repository.
2. Copy the contents of this pack's `src/capitaldynamics/` into the existing `src/capitaldynamics/` package, replacing the corresponding analysis entry points and adding the new subpackages.
3. **Keep the existing** `src/capitaldynamics/data/marts.py` from the repository. The CLI's `build-marts` command expects it to provide `build_marts(warehouse=...)`.
4. Merge the dependency and project-script entries from `pyproject.toml` into the repository's actual project configuration. Do not replace project metadata or unrelated development tooling blindly.
5. From the repository root, install dependencies and the package. For example, with uv:

   ```bash
   uv sync --extra dev
   ```

6. Run the tests:

   ```bash
   uv run pytest
   ```

7. Build marts using the existing source observations:

   ```bash
   uv run capitaldynamics build-marts
   ```

8. Verify the semantic dataset:

   ```bash
   uv run capitaldynamics inspect
   ```

The pack assumes that the existing upstream ingestion step has already populated `raw.observations`. It does not schedule or initiate collection.

## Running analyses

Acquisition:

```bash
uv run capitaldynamics acquisition \
  --gamma 1947=0.90 \
  --gamma 1970=1.05
```

Retirement:

```bash
uv run capitaldynamics retirement \
  --start-year 1947 \
  --gamma 1947=0.90 \
  --gamma 1970=1.05
```

Both commands are non-interactive. By default, each run is written under:

```text
data/outputs/<analysis>/<UTC timestamp>/
├── results.csv
├── manifest.json
└── *.png
```

An explicit `--output-dir` can be supplied, but it must not already exist. This prevents an accidental rerun from overwriting prior output. `--show` is optional for desktop use and should be omitted in scheduled/headless execution.

The same commands can be invoked as modules:

```bash
uv run python -m capitaldynamics acquisition --gamma 1947=0.90
uv run python -m capitaldynamics retirement --start-year 1947 --gamma 1947=0.90
```

## Unattended operation

For a scheduled job:

- Supply the Gamma schedule explicitly in the scheduler's command or a version-controlled deployment wrapper.
- Use an absolute warehouse path when the scheduler's working directory is not the repository root.
- Omit `--show`.
- Treat a non-zero exit status as a failed run and alert on it.
- Preserve the run directory and manifest as the reproducibility record.
- Back up the DuckDB warehouse and monitor available disk space.
- Pin exact dependency versions in the deployment lockfile (`uv.lock`) and commit that lockfile. This pack intentionally does not invent a lockfile without resolving against the actual target platform.
- Schedule ingestion/mart construction before analysis, with explicit failure handling between steps. Do not run analysis against a partially refreshed source dataset.
- If two invocations may start concurrently, use a scheduler-level single-instance policy. Timestamped run directories prevent ordinary overwrite, but do not replace orchestration-level concurrency control.

There is no automatic retention deletion. This is deliberate: a scheduled analysis should not silently remove historical results. Establish a documented backup and retention policy outside the calculation package.

## What is intentionally not included

The supplied files did not show the upstream BEA/data collection code, its API configuration, retry policy, or any project-specific deployment configuration. This pack therefore does not modify those components. The existing mart compiler is also retained as-is. A full repository-level hardening pass should inspect those files and the actual `pyproject.toml`, lockfile, tests, and scheduler/deployment setup before declaring the whole project unattended-ready.

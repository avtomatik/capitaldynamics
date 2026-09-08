import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .application.scenario import Scenario
from .data.csv import load_table
from .domain.acquisition import calculate_acquisition
from .domain.retirement import calculate_retirement
from .visualization import acquisition as acquisition_plot
from .visualization import retirement as retirement_plot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="capital")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("acquisition", "retirement"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--input", required=True, type=Path)
        cmd.add_argument("--config", required=True, type=Path)
        cmd.add_argument("--output", type=Path)
        cmd.add_argument("--plot-dir", type=Path)
        cmd.add_argument("--show", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dataset = load_table(args.input)
    scenario = Scenario.from_yaml(args.config)
    if args.command == "acquisition":
        result = calculate_acquisition(
            dataset, scenario.analysis_start, scenario.gamma
        )
        figs = acquisition_plot.figures(result)
    else:
        result = calculate_retirement(
            dataset, scenario.analysis_start, scenario.gamma
        )
        figs = retirement_plot.figures(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        result.table().to_csv(args.output, index=False)
    if args.plot_dir:
        saver = (
            acquisition_plot.save
            if args.command == "acquisition"
            else retirement_plot.save
        )
        saver(figs, args.plot_dir)
    if args.show:
        plt.show()
    else:
        for fig in figs:
            plt.close(fig)
    print(
        f"analysis={args.command} scenario={scenario.name} analysis_start={result.analysis_start} base_year={result.base_year}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

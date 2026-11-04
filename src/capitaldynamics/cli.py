import argparse
import sys
from pathlib import Path

from capitaldynamics.analysis.segmentation import GammaSchedule
from capitaldynamics.config.paths import WAREHOUSE


def _parse_gamma(values: list[str]) -> GammaSchedule:
    pairs: list[tuple[int, float]] = []
    for value in values:
        try:
            year_text, gamma_text = value.split("=", maxsplit=1)
            pairs.append((int(year_text.strip()), float(gamma_text.strip())))
        except (ValueError, TypeError) as exc:
            raise argparse.ArgumentTypeError(
                f"Invalid Gamma breakpoint {value!r}; use YEAR=VALUE, "
                "for example --gamma 1947=0.95."
            ) from exc
    try:
        return GammaSchedule.from_pairs(pairs)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _add_analysis_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--gamma",
        action="append",
        required=True,
        metavar="YEAR=VALUE",
        help=(
            "Gamma value active from this source year. Repeat for changes, "
            "for example --gamma 1947=0.9 --gamma 1970=1.05."
        ),
    )
    parser.add_argument(
        "--warehouse",
        type=Path,
        default=WAREHOUSE,
        help=f"DuckDB warehouse (default: {WAREHOUSE}).",
    )
    parser.add_argument(
        "--relation",
        default="marts.capital_dynamics_archived",
        help="Schema-qualified DuckDB relation to analyse.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "New output directory. "
            "By default a UTC timestamped run directory is used."
        ),
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help=(
            "Display plots after saving them "
            "(not suitable for unattended runs)."
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="capitaldynamics",
        description=(
            "Reproducible capital acquisition and retirement analysis."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    acquisition = subparsers.add_parser(
        "acquisition",
        help="Analyse capital acquisition and capacity indicators.",
    )
    _add_analysis_arguments(acquisition)
    retirement = subparsers.add_parser(
        "retirement", help="Analyse capital retirement indicators."
    )
    _add_analysis_arguments(retirement)
    retirement.add_argument(
        "--start-year",
        type=int,
        default=None,
        help=(
            "First year included in the retirement analysis "
            "(default: first year)."
        ),
    )
    marts = subparsers.add_parser(
        "build-marts",
        help="Build existing configured marts from raw.observations.",
    )
    marts.add_argument("--warehouse", type=Path, default=WAREHOUSE)
    inspect = subparsers.add_parser(
        "inspect",
        help="Print row count and year range for the semantic dataset.",
    )
    inspect.add_argument("--warehouse", type=Path, default=WAREHOUSE)
    inspect.add_argument(
        "--relation", default="marts.capital_dynamics_archived"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "build-marts":
            # The mart compiler is intentionally kept as the existing project
            # module: its ingestion and reconstruction definitions were not in
            # the supplied code excerpt and should not be replaced blindly.
            from capitaldynamics.data.marts import build_marts

            build_marts(warehouse=args.warehouse)
            print(f"Marts built successfully in {args.warehouse}")
            return 0
        if args.command == "inspect":
            from capitaldynamics.data.loader import load_data

            frame = load_data(warehouse=args.warehouse, relation=args.relation)
            print(f"Relation: {args.relation}")
            print(f"Rows: {len(frame)}")
            print(f"Years: {frame.index.min()}–{frame.index.max()}")
            print(f"Columns: {', '.join(frame.columns)}")
            return 0
        try:
            schedule = _parse_gamma(args.gamma)
        except argparse.ArgumentTypeError as exc:
            parser.error(str(exc))
        # Select a non-interactive backend before importing pyplot through the
        # visualization modules. --show opts into the user's GUI backend.
        if not args.show:
            import matplotlib

            matplotlib.use("Agg", force=True)
        if args.command == "acquisition":
            from capitaldynamics.workflow.acquisition import (
                run_acquisition_analysis,
            )

            artifacts = run_acquisition_analysis(
                schedule,
                warehouse=args.warehouse,
                output_dir=args.output_dir,
                relation=args.relation,
                show=args.show,
            )
        elif args.command == "retirement":
            from capitaldynamics.workflow.retirement import (
                run_retirement_analysis,
            )

            artifacts = run_retirement_analysis(
                schedule,
                warehouse=args.warehouse,
                output_dir=args.output_dir,
                relation=args.relation,
                start_year=args.start_year,
                show=args.show,
            )
        else:  # pragma: no cover - argparse constrains the command set
            parser.error(f"Unsupported command: {args.command}")
            return 2
        print(f"Analysis complete: {artifacts.row_count} annual observations")
        print(f"Output directory: {artifacts.output_dir}")
        print(f"Results: {artifacts.results_csv}")
        print(f"Manifest: {artifacts.manifest}")
        print(f"Charts: {len(artifacts.figures)}")
        return 0
    except (
        ValueError,
        RuntimeError,
        FileNotFoundError,
        FileExistsError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

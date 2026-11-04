import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure

from capitaldynamics.config.paths import OUTPUTS_DIR
from capitaldynamics.visualization.common import close_figures


@dataclass(frozen=True)
class RunArtifacts:
    output_dir: Path
    results_csv: Path
    manifest: Path
    figures: tuple[Path, ...]
    row_count: int


def default_run_directory(analysis_name: str) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    return OUTPUTS_DIR / analysis_name / timestamp


def persist_run(
    *,
    analysis_name: str,
    result: pd.DataFrame,
    figures: dict[str, Figure],
    metadata: dict[str, object],
    output_dir: Path | None = None,
    show: bool = False,
) -> RunArtifacts:
    """Write a complete run into a staging directory, then publish atomically.
    A run directory is never overwritten. This prevents a repeated scheduled
    invocation from silently destroying an earlier result.
    """
    final_dir = (
        Path(output_dir)
        if output_dir is not None
        else default_run_directory(analysis_name)
    )
    final_dir = final_dir.expanduser().resolve()
    final_dir.parent.mkdir(parents=True, exist_ok=True)
    if final_dir.exists():
        close_figures(figures)
        raise FileExistsError(
            f"Output directory already exists: {final_dir}. "
            "Choose a new --output-dir; existing runs are never overwritten."
        )
    staging_dir = Path(
        tempfile.mkdtemp(prefix=f".{final_dir.name}.", dir=final_dir.parent)
    )
    figure_paths: list[Path] = []
    try:
        results_path = staging_dir / "results.csv"
        result.to_csv(results_path, index=False, float_format="%.12g")
        for name, figure in figures.items():
            path = staging_dir / f"{name}.png"
            figure.savefig(path, format="png", dpi=160, bbox_inches="tight")
            figure_paths.append(final_dir / path.name)
        manifest_data = {
            "analysis": analysis_name,
            "created_at_utc": datetime.now(UTC).isoformat(),
            "row_count": int(len(result)),
            "first_year": int(result["year"].iloc[0]),
            "last_year": int(result["year"].iloc[-1]),
            **metadata,
        }
        manifest_path = staging_dir / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest_data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        # Same-filesystem directory rename publishes CSV, figures and manifest
        # together; consumers never see a partially written run directory.
        os.replace(staging_dir, final_dir)
    except Exception:
        shutil.rmtree(staging_dir, ignore_errors=True)
        close_figures(figures)
        raise
    if show:
        import matplotlib.pyplot as plt

        plt.show()
    close_figures(figures)
    return RunArtifacts(
        output_dir=final_dir,
        results_csv=final_dir / "results.csv",
        manifest=final_dir / "manifest.json",
        figures=tuple(figure_paths),
        row_count=len(result),
    )

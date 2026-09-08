from pathlib import Path

import pandas as pd

from ..domain.models import CapitalDataset


def load_table(path: str | Path) -> CapitalDataset:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported input format: {path.suffix}")
    return CapitalDataset.from_frame(frame)

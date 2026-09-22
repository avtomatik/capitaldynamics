from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
WAREHOUSE = DATA_DIR / "warehouse" / "observations.duckdb"

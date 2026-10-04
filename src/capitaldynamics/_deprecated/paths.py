from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
WAREHOUSE = BASE_DIR / "data" / "warehouse" / "observations.duckdb"

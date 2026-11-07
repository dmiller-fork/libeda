import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

df = pd.read_csv(
    RAW_DIR / "application_data.csv",
    low_memory=False,
    dtype={"examiner_id": "string"}
)

df.to_csv(STAGED_DIR / "stg_appdata.csv", index=False)


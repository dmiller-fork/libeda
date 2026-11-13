import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STAGED_DIR = PROJECT_ROOT / "data" / "staged"
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
stg = pd.read_csv(
	STAGED_DIR / "stg_appdata.csv",
	usecols=["application_number"],
	low_memory=False
)
data = pd.read_csv(
	DERIVED_DIR / "mart_disposalcounts.csv"
)

source_count = len(stg)
result_count = data["total_ct"].sum()

print(data.to_string(index=False))

print(f"\nSource population: {source_count:,}")
print(f"Analysis population: {result_count:,}")
print(f"Excluded count: {source_count - result_count:,}")

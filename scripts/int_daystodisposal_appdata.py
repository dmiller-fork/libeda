import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def days_to_disposal(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()

	df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
	df["abandon_date"] = pd.to_datetime(df["abandon_date"], errors="coerce")
	df["patent_issue_date"] = pd.to_datetime(df["patent_issue_date"], errors="coerce")

	disposal_date = df["abandon_date"].fillna(df["patent_issue_date"])

	return (
		df.assign(
			days_to_disposal=(disposal_date - df["filing_date"]).dt.days
		)[["application_number", "days_to_disposal"]]
	)


df = pd.read_csv(STAGED_DIR / "stg_appdata.csv", low_memory=False)
result = days_to_disposal(df)
result.to_csv(DERIVED_DIR / "int_daystodisposal_appdata.csv", index=False)

print(result["days_to_disposal"].describe())

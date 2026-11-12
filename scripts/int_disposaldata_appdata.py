import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def disposal_data(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()

	df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
	df["abandon_date"] = pd.to_datetime(df["abandon_date"], errors="coerce")
	df["patent_issue_date"] = pd.to_datetime(df["patent_issue_date"], errors="coerce")

	disposal_date = df["abandon_date"].fillna(df["patent_issue_date"])
	disposal_type = df["abandon_date"].notna().map({
		True: "abandoned",
		False: "issued"
	})
	return df.assign(
		days_to_disposal=(disposal_date - df["filing_date"]).dt.days,
		disposal_year=disposal_date.dt.year.astype("Int64"),
		disposal_type=disposal_type
	)[[
		"application_number",
		"days_to_disposal",
		"disposal_year",
		"disposal_type"
	]]

def disposal_cohort(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()

	df["disposal_cohort"] = (
		((df["disposal_year"] - 2000) // 4) * 4 + 2000
	)

	return df

df = pd.read_csv(STAGED_DIR / "stg_appdata.csv", low_memory=False)
result = disposal_data(df)
result = disposal_cohort(result)
result.to_csv(DERIVED_DIR / "int_disposaldata_appdata.csv", index=False)

print(result["days_to_disposal"].describe())
print(result["disposal_year"].describe())

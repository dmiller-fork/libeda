import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def allowance_rate(df: pd.DataFrame, examiner_df: pd.DataFrame) -> pd.DataFrame:
	df = df.merge(
		examiner_df[["examiner_id", "issue_ct", "total_ct"]],
		on="examiner_id",
		how="left"
	)

	return df.assign(
		allowance_rate=df["issue_ct"] / df["total_ct"]
	)[["application_number", "allowance_rate"]]

appdata = pd.read_csv(
		STAGED_DIR / "stg_appdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
examinerdata = pd.read_csv(
		DERIVED_DIR / "int_examinerid_appdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
assert examinerdata["examiner_id"].is_unique, "Duplicate examiner_id values detected"
result = allowance_rate(appdata, examinerdata)
result.to_csv(DERIVED_DIR / "int_allowancerate_appdata.csv", index=False)

print(result["allowance_rate"].describe())

import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def join_allowancedata(appdata: pd.DataFrame, examinerdata: pd.DataFrame) -> pd.DataFrame:
	return appdata.merge(
		examinerdata[["examiner_id", "allowance_rate", "allowance_group"]],
		on="examiner_id",
		how="left"
	)[["application_number", "allowance_rate", "allowance_group"]]

appdata = pd.read_csv(
		STAGED_DIR / "stg_appdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
examinerdata = pd.read_csv(
		DERIVED_DIR / "int_allowancerate_examinerdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
assert examinerdata["examiner_id"].is_unique, "Duplicate examiner_id values detected"
result = join_allowancedata(appdata, examinerdata)
result.to_csv(DERIVED_DIR / "int_allowancerate_appdata.csv", index=False)

print(result["allowance_rate"].describe())

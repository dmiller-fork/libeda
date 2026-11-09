import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

from libeda import Analysis
from libeda import Clean
from libeda import Transform

def create_examiner_table(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()
	return (
		df.assign(
			issue_ct=df["patent_issue_date"].notna().astype(int),
			abandon_ct=df["abandon_date"].notna().astype(int),
			total_ct=1
		)
		.groupby("examiner_id", as_index=False)
		[["issue_ct", "abandon_ct", "total_ct"]]
		.sum()
	)

if __name__ == "__main__":

	appdata = pd.read_csv(
		STAGED_DIR / "stg_appdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
	daystodisposal = pd.read_csv(DERIVED_DIR / "int_daystodisposal_appdata.csv",
		dtype={"application_number": str}
	)
	result = Transform.join(
		daystodisposal,
		"application_number",
		appdata,
		"application_number"
	)
	print("after join: ", Analysis.count_rows(result))

	result = Clean.remove_null(result, "days_to_disposal")
	print("after cleaning null row_count: ", Analysis.count_rows(result))
	result = Clean.remove_negative(result, "days_to_disposal")
	print("after cleaning negative row_count: ", Analysis.count_rows(result))

	result = Clean.remove_nonexclusive(result,"patent_issue_date", "abandon_date")
	is_valid = Analysis.validate_exclusive(result, "patent_issue_date", "abandon_date")
	print("patent_issue_date and abandon_date are mutually exclusive: ", is_valid)
	result = create_examiner_table(result)

	assert (result["total_ct"] == result["issue_ct"] + result["abandon_ct"]).all()
	result.to_csv(DERIVED_DIR / "int_examinerid_appdata.csv", index=False)

	print(result.describe())

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

from libeda import Transform

if __name__ == "__main__":
	
	appdata = pd.read_csv(STAGED_DIR / "stg_appdata.csv", low_memory=False)
	daystodisposal = pd.read_csv(DERIVED_DIR / "int_daystodisposal_appdata.csv",
		dtype={"application_number": str}
	)

	app_id = "02509599"

	print(appdata["application_number"].dtype)
	print(daystodisposal["application_number"].dtype)

	print(app_id in appdata["application_number"].values)
	print(app_id in daystodisposal["application_number"].values)
	print(Transform.lookup(appdata, "application_number", app_id))
	print(Transform.lookup(daystodisposal, "application_number", app_id))
	print(
		Transform.lookup(appdata, "application_number", app_id)[
			["application_number", "earliest_pgpub_number", "filing_date",
			 "patent_issue_date", "abandon_date"]
		].to_string(index=False)
	)

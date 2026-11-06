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
from libeda import Analysis
from libeda import Clean

if __name__ == "__main__":
	
	appdata = pd.read_csv(STAGED_DIR / "stg_appdata.csv", low_memory=False)
	daystodisposal = pd.read_csv(DERIVED_DIR / "int_daystodisposal_appdata.csv",
		dtype={"application_number": str}
	)
	print("starting row_count: ", Analysis.count_rows(daystodisposal))
	result = Clean.remove_null(daystodisposal, "days_to_disposal")
	print("after cleaning null row_count: ", Analysis.count_rows(result))
	result2 = Clean.remove_negative(daystodisposal, "days_to_disposal")
	print("after cleaning negative row_count: ", Analysis.count_rows(result2))
	result3 = Transform.join(
		result2,
		"application_number", 
		appdata,
		"application_number"
	)
	print("after join: ", Analysis.count_rows(result3))
	result4 = Transform.project(result3, 10, ["application_number", "days_to_disposal"])
	print(result4)


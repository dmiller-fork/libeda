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
	result = Clean.remove_nonexclusive(
		appdata,
		"patent_issue_date",
		"abandon_date"
	)

	print(f"Original rows: {len(appdata)}")
	print(f"Remaining rows: {len(result)}")
	print(f"Removed rows: {len(appdata) - len(result)}")

	Analysis.validate_exclusive(result, "patent_issue_date", "abandon_date")

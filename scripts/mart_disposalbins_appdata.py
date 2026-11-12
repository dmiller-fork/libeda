import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def join_disposaldata(appdata, disposaldata):
    return appdata.merge(
        disposaldata[
            ["application_number", "disposal_type", "disposal_cohort"]
        ],
        on="application_number",
        how="left"
    )[
        ["application_number", "disposal_type",
         "disposal_cohort", "allowance_group"]
    ]

appdata = pd.read_csv(
		DERIVED_DIR / "int_allowancerate_appdata.csv",
		low_memory=False
	)
disposaldata = pd.read_csv(
		DERIVED_DIR / "int_disposaldata_appdata.csv",
		low_memory=False
	)
result = join_disposaldata(appdata, disposaldata)
result.to_csv(DERIVED_DIR / "mart_disposalbins_appdata.csv", index=False)
counts = result.groupby(
    ["disposal_type", "disposal_cohort", "allowance_group"]
).size().reset_index(name="count")

print(counts.to_string(index=False))

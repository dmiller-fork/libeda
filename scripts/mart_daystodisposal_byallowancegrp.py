import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
from libeda import Clean

# Load disposal bins
bins = pd.read_csv(
	DERIVED_DIR / "mart_disposalbins_appdata.csv",
	usecols=[
		"application_number",
		"disposal_cohort",
		"disposal_type",
		"allowance_group"
	],
	dtype={"application_number": "string"},
	low_memory=False
)

# Load disposal data
disposal = pd.read_csv(
	DERIVED_DIR / "int_disposaldata_appdata.csv",
	usecols=[
		"application_number",
		"days_to_disposal"
	],
	dtype={"application_number": "string"},
	low_memory=False
)

# Join
data = bins.merge(
	disposal,
	on="application_number",
	how="inner"
)

# Aggregate
counts = (
	data.groupby(
		["disposal_cohort", "allowance_group", "disposal_type"],
		observed=True
	)
	.agg(
		days_mean=("days_to_disposal", "mean"),
		days_median=("days_to_disposal", "median"),
		days_std=("days_to_disposal", "std"),
		total_ct=("days_to_disposal", "count")
	)
	.reset_index()
)

# Clean cohort range
counts["disposal_cohort"] = (
    counts["disposal_cohort"].astype("Int64")
)

counts = Clean.remove_outsiderange(
    counts, "disposal_cohort", 1980, 2016
)

counts = Clean.remove_lowerbound(
	counts, "total_ct", 30
)

counts.to_csv(
    DERIVED_DIR / "mart_daystodisposal_byallowancegrp.csv",
    index=False
)

print(counts.to_string(index=False))

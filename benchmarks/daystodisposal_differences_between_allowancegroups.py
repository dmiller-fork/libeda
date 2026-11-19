import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

data = pd.read_csv(
	DERIVED_DIR / "mart_daystodisposal_byallowancegrp.csv"
)

pairs = [
	("90-99.99", "80-89.99"),
	("80-89.99", "70-79.99"),
	("70-79.99", "60-69.99"),
	("60-69.99", "50-59.99"),
	("50-59.99", "40-49.99"),
	("40-49.99", "30-39.99"),
	("30-39.99", "20-29.99"),
	("20-29.99", "10-19.99"),
]

for cohort in [2008, 2012, 2016]:
	subset = data[
		(data["disposal_cohort"] == cohort) &
		(data["disposal_type"] == "abandoned")
	]

	values = subset.set_index("allowance_group")["days_median"]

	print(f"\nCohort: {cohort}")

	for high, low in pairs:
		difference = values[high] - values[low]
		print(f"{high} minus {low}: {difference:.2f} days")



print("\nREGIONAL AVERAGE ABSOLUTE DIFFERENCES")

upper_pairs = [
    ("90-99.99", "80-89.99"),
    ("80-89.99", "70-79.99"),
    ("70-79.99", "60-69.99"),
]

lower_pairs = [
	("60-69.99", "50-59.99"),
    ("50-59.99", "40-49.99"),
    ("40-49.99", "30-39.99"),
    ("30-39.99", "20-29.99"),
    ("20-29.99", "10-19.99"),
]

for cohort in [2008, 2012, 2016]:
    subset = data[
        (data["disposal_cohort"] == cohort) &
        (data["disposal_type"] == "abandoned")
    ]

    values = subset.set_index("allowance_group")["days_median"]

    upper_diffs = [
        abs(values[high] - values[low])
        for high, low in upper_pairs
    ]

    lower_diffs = [
        abs(values[high] - values[low])
        for high, low in lower_pairs
    ]

    print(f"\nCohort: {cohort}")
    print(f"Upper region (60-100%): {np.mean(upper_diffs):.2f} days")
    print(f"Lower region (0-60%): {np.mean(lower_diffs):.2f} days")


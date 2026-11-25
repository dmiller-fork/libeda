
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

# Load application-level data
data = pd.read_csv(
	DERIVED_DIR / "mart_join_all.csv",
	dtype={"application_number": "string"},
	low_memory=False
)

print(data["allowance_rate"].describe())
print("\nUnique allowance rates:", data["allowance_rate"].nunique())

print("\nVariation within groups:")
print(
    data.groupby(
        ["disposal_cohort", "disposal_type", "allowance_group"]
    )["allowance_rate"].agg(
        ["count", "nunique", "min", "max", "std"]
    ).head(20).to_string()
)

group_columns = [
	"disposal_cohort",
	"disposal_type",
	# "allowance_group"
]

variables = [
	"days_to_disposal",
	"citation_count",
	"form892_citation_count",
	"office_action_count"
]

results = []

# Calculate Pearson correlations within each group
for group_values, group in data.groupby(group_columns):

	for variable in variables:

		subset = group[
			["allowance_rate", variable]
		].dropna()

		n = len(subset)

		if n < 2:
			r = float("nan")
		else:
			r = subset["allowance_rate"].corr(
				subset[variable],
				method="pearson"
			)

		results.append({
			"disposal_cohort": group_values[0],
			"disposal_type": group_values[1],
		#	"allowance_group": group_values[2],
			"variable": variable,
			"pearson_r": r,
			"n": n
		})

# Create results dataframe
results = pd.DataFrame(results)

# Export
"""
results.to_csv(
	DERIVED_DIR / "mart_pearson_correlations.csv",
	index=False
)
"""

print(results.to_string(index=False))
print(f"\nTotal correlations calculated: {len(results):,}")



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

# Grouping dimensions
group_columns = [
	"disposal_cohort",
	"disposal_type"
]

# Variables to correlate against allowance_rate
variables = [
	"days_to_disposal",
	"citation_count",
	"form892_citation_count",
	"office_action_count"
]

# Candidate breakpoints
breakpoints = [i / 100 for i in range(10, 100, 10)]

# Minimum observations per supergroup
MIN_N = 100

results = []

# Iterate through cohorts and disposal types
for group_values, group in data.groupby(group_columns):

	for breakpoint in breakpoints:

		# Divide into two allowance supergroups
		lower = group[group["allowance_rate"] < breakpoint]
		upper = group[group["allowance_rate"] >= breakpoint]

		supergroups = {
			"below": lower,
			"above": upper
		}

		for side, subset in supergroups.items():

			for variable in variables:

				paired = subset[
					["allowance_rate", variable]
				].dropna()

				n = len(paired)

				if n < MIN_N:
					r = float("nan")
				elif paired["allowance_rate"].nunique() < 2:
					r = float("nan")
				elif paired[variable].nunique() < 2:
					r = float("nan")
				else:
					r = paired["allowance_rate"].corr(
						paired[variable],
						method="pearson"
					)

				results.append({
					"disposal_cohort": group_values[0],
					"disposal_type": group_values[1],
					"breakpoint": breakpoint,
					"side": side,
					"variable": variable,
					"pearson_r": r,
					"n": n
				})

# Create results dataframe
results = pd.DataFrame(results)

# Export results
output = DERIVED_DIR / "mart_pearson_breakpoints.csv"
results.to_csv(output, index=False)
"""
print(results.to_string(index=False))
print(f"\nTotal correlations: {len(results):,}")
# print(f"Output: {output}")
# Filter results for correlations above 0.05 (absolute value)
filtered = results[results["pearson_r"].abs() > 0.2]

print(filtered.to_string(index=False))
print(f"\nCorrelations above threshold: {len(filtered):,}")
"""
# Remove undefined correlations
valid = results.dropna(subset=["pearson_r"]).copy()

valid = valid[
    (valid["disposal_type"] == "abandoned") &
    (valid["side"] == "above") &
    (valid["pearson_r"].abs() > 0.1)
]

# Find strongest absolute correlation per category
idx = valid.groupby(
    ["disposal_cohort", "disposal_type", "variable"]
)["pearson_r"].apply(lambda x: x.abs().idxmax())

strongest = valid.loc[idx.values].sort_values(
    ["disposal_cohort", "disposal_type", "variable"]
)

print(strongest.to_string(index=False))

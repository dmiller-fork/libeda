import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

data = pd.read_csv(
	DERIVED_DIR / "mart_daystodisposal_byallowancegrp.csv"
)

allowance_groups = [
	f"{i}-{i+9}.99" for i in range(0, 100, 10)
]

cohorts = sorted(data["disposal_cohort"].dropna().unique())

for cohort in cohorts:
	subset = (
		data[
			(data["disposal_cohort"] == cohort) &
			(data["disposal_type"] == "abandoned")
		]
		.set_index("allowance_group")
		.reindex(allowance_groups)
	)

	subset["slope"] = (
		subset["days_median"].diff() / 10
	)

	print(f"\nCohort: {int(cohort)}")
	print(subset[["days_median", "slope"]].to_string())

	x = np.arange(len(allowance_groups))

	fig, ax = plt.subplots(figsize=(12, 6))

	ax.plot(
		x, subset["slope"],
		marker="o",
		label="Slope"
	)

	ax.axhline(0, color="black", linewidth=0.8)

	ax.set_title(
		f"Change in Median Days to Disposal: {int(cohort)}"
	)
	ax.set_xlabel("Allowance Group (%)")
	ax.set_ylabel("Change in Days per Allowance Percentage Point")
	ax.set_xticks(x)
	ax.set_xticklabels(allowance_groups, rotation=45)
	ax.legend()

	plt.tight_layout()
	plt.show()


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

cohorts = [2008, 2012, 2016]

for cohort in cohorts:
	subset = (
		data[data["disposal_cohort"] == cohort]
		.pivot(
			index="allowance_group",
			columns="disposal_type",
			values="days_mean"
		)
		.reindex(allowance_groups)
	)

	subset["difference"] = (
		subset["abandoned"] - subset["issued"]
	)

	print(f"\nCohort: {int(cohort)}")
	print(subset[["issued", "abandoned", "difference"]].to_string())

	x = np.arange(len(allowance_groups))

	fig, ax = plt.subplots(figsize=(12, 6))

	ax.plot(
		x, subset["issued"],
		marker="o",
		label="Issued"
	)

	ax.plot(
		x, subset["abandoned"],
		marker="o",
		label="Abandoned"
	)

	ax.plot(
		x, subset["difference"],
		marker="s",
		linestyle="--",
		label="Difference (Abandoned - Issued)"
	)

	ax.axhline(0, color="black", linewidth=0.8)

	ax.set_title(f"Mean Days to Disposal: {int(cohort)}")
	ax.set_xlabel("Allowance Group (%)")
	ax.set_ylabel("Days to Disposal")
	ax.set_xticks(x)
	ax.set_xticklabels(allowance_groups, rotation=45)
	ax.legend()

	plt.tight_layout()
	plt.show()


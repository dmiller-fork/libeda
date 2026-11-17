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
		data[data["disposal_cohort"] == cohort]
		.pivot(
			index="allowance_group",
			columns="disposal_type",
			values="days_mean"
		)
		.reindex(allowance_groups)
	)

	x = np.arange(len(allowance_groups))
	width = 0.4

	fig, ax = plt.subplots(figsize=(12, 6))

	issued_max = subset["issued"].max()
	abandoned_max = subset["abandoned"].max()

	issued_norm = (
		subset["issued"] / issued_max * 100
	)

	abandoned_norm = (
		subset["abandoned"] / abandoned_max * 100
	)

	ax.bar(
		x - width / 2,
		issued_norm,
		width,
		label="Issued_normalized"
	)

	ax.bar(
		x + width / 2,
		abandoned_norm,
		width,
		label="Abandoned_normalized"
	)

	ax.set_title(f"Mean Days to Disposal: {int(cohort)}")
	ax.set_xlabel("Allowance Group (%)")
	ax.set_ylabel("Mean Days to Disposal Normalized")
	ax.set_xticks(x)
	ax.set_xticklabels(allowance_groups, rotation=45)
	ax.legend()

	plt.tight_layout()
	plt.show()

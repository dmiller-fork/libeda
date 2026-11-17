import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

data = pd.read_csv(
	DERIVED_DIR / "mart_disposalcounts_byallowancegrp.csv"
)

allowance_groups = [
	f"{i}-{i+9}.99" for i in range(0, 100, 10)
]

cohorts = sorted(data["disposal_cohort"].dropna().unique())

for cohort in cohorts:
	subset = (
		data[data["disposal_cohort"] == cohort]
		.set_index("allowance_group")
		.reindex(allowance_groups, fill_value=0)
	)

	x = np.arange(len(allowance_groups))
	width = 0.4

	fig, ax = plt.subplots(figsize=(12, 6))
	
	issued_total = subset["issued_ct"].sum()
	abandoned_total = subset["abandoned_ct"].sum()

	issued_pct = (
		subset["issued_ct"] / issued_total * 100
		if issued_total > 0
		else subset["issued_ct"] * 0
	)

	abandoned_pct = (
		subset["abandoned_ct"] / abandoned_total * 100
		if abandoned_total > 0
		else subset["abandoned_ct"] * 0
	)
	ax.bar(
		x - width / 2,
		issued_pct,
		width,
		label="Issued"
	)
	ax.bar(
		x + width / 2,
		abandoned_pct,
		width,
		label="Abandoned"
	)

	ax.set_title(f"Disposed Applications: {int(cohort)}")
	ax.set_xlabel("Allowance Group (%)")
	ax.set_ylabel("Relative Frequency (%)")
	ax.set_xticks(x)
	ax.set_xticklabels(allowance_groups, rotation=45)
	ax.legend()

	plt.tight_layout()
	plt.show()


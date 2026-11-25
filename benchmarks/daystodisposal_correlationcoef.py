import numpy as np
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

from libeda import Transform
from libeda import Analysis
from libeda import Clean

data = pd.read_csv(
	DERIVED_DIR / "mart_daystodisposal_byallowancegrp.csv"
)
for cohort in [2008, 2012, 2016]:
	subset = data[
		(data["disposal_cohort"] == cohort) &
		(data["disposal_type"] == "abandoned")
	].copy()

	subset["allowance_rate"] = (
		subset["allowance_group"]
		.str.split("-")
		.str[0]
		.astype(float)
	)

	r = Analysis.correlation_coef(
		subset["allowance_rate"],
		subset["days_median"]
	)

	print(f"Cohort: {cohort}, Pearson r: {r.statistic:.4f}")

groups = [
	"90-99.99",
	"80-89.99",
	"70-79.99",
	"60-69.99",
	"50-59.99",
	"40-49.99",
	"30-39.99",
	"20-29.99",
	"10-19.99",
]

for cohort in [2008, 2012, 2016]:
	subset = data[
		(data["disposal_cohort"] == cohort) &
		(data["disposal_type"] == "abandoned")
	].copy()

	subset["allowance_rate"] = (
		subset["allowance_group"]
		.str.split("-").str[0].astype(float)
	)

	subset = subset.set_index("allowance_group")

	print(f"\nCOHORT: {cohort}")

	for n in range(2, len(groups)-1):
		selected = subset.loc[groups[:n]]
		other_group = subset.loc[groups[n:]]
		
		r = Analysis.correlation_coef(
			selected["allowance_rate"],
			selected["days_median"]
		)

		r2 = Analysis.correlation_coef(
			other_group["allowance_rate"],
			other_group["days_median"]
		)

		print(
			f"Upper: {n} groups | "
			f"Breakpoint: {groups[n-1]} | "
			f"r: {r.statistic:.4f}"
		)

		print(
			f"Lower: {len(groups)-n} groups | "
			f"Breakpoint: {groups[n-1]} | "
			f"r: {r2.statistic:.4f}"
		)

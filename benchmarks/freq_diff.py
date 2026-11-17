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

data["relative_freq_issued"] = (
    data["issued_ct"]
    / data.groupby("disposal_cohort")["issued_ct"].transform("sum")
)

data["relative_freq_abandoned"] = (
    data["abandoned_ct"]
    / data.groupby("disposal_cohort")["abandoned_ct"].transform("sum")
)

data["relative_freq_diff"] = (
    data["relative_freq_issued"]
    - data["relative_freq_abandoned"]
)
pct_cols = [
    "relative_freq_issued",
    "relative_freq_abandoned",
    "relative_freq_diff",
]

data[pct_cols] = data[pct_cols] * 100

print(
    data[
        [
            "disposal_cohort",
            "allowance_group",
            *pct_cols,
        ]
    ].round(2).to_string(index=False)
)

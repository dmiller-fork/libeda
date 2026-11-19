
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

data = pd.read_csv(
    DERIVED_DIR / "mart_daystodisposal_byallowancegrp.csv"
)

for cohort in [2008, 2012, 2016]:
    subset = data[
        (data["disposal_cohort"] == cohort) &
        (data["disposal_type"] == "abandoned") &
        (data["allowance_group"].isin(["80-89.99", "90-99.99"]))
    ]

    values = subset.set_index("allowance_group")["days_median"]

    difference = values["90-99.99"] - values["80-89.99"]

    print(f"{cohort}: {difference:.2f} days")


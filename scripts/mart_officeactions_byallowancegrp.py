import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
STAGED_DIR = PROJECT_ROOT / "data" / "staged"

from libeda import Clean

# Load disposal bins
bins = pd.read_csv(
    DERIVED_DIR / "mart_disposalbins_appdata.csv",
    usecols=[
        "application_number",
        "disposal_cohort",
        "disposal_type",
        "allowance_group"
    ],
    dtype={"application_number": "string"},
    low_memory=False
)

# Load office actions
office_actions = pd.read_csv(
    STAGED_DIR / "stg_officeactions.csv",
    usecols=["app_id"],
    dtype={"app_id": "string"},
    low_memory=False
)

# Aggregate office actions by application
office_action_counts = (
    office_actions.groupby("app_id")
    .size()
    .reset_index(name="office_action_count")
    .rename(columns={"app_id": "application_number"})
)

# Join
data = bins.merge(
    office_action_counts,
    on="application_number",
    how="inner"
)

# Aggregate
counts = (
    data.groupby(
        ["disposal_cohort", "allowance_group", "disposal_type"],
        observed=True
    )
    .agg(
        office_actions_mean=("office_action_count", "mean"),
        office_actions_median=("office_action_count", "median"),
        office_actions_std=("office_action_count", "std"),
        total_ct=("office_action_count", "count")
    )
    .reset_index()
)

# Clean cohort range
counts["disposal_cohort"] = (
    counts["disposal_cohort"].astype("Int64")
)

counts = Clean.remove_outsiderange(
    counts, "disposal_cohort", 2008, 2016
)

counts = Clean.remove_lowerbound(
    counts, "total_ct", 30
)

counts.to_csv(
    DERIVED_DIR / "mart_officeactions_byallowancegrp.csv",
    index=False
)

print(counts.to_string(index=False))

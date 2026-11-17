
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
from libeda import Clean

data = pd.read_csv(
    DERIVED_DIR / "mart_disposalbins_appdata.csv",
    usecols=[
        "disposal_cohort",
        "disposal_type",
        "allowance_group"
    ]
)

# Aggregate counts
counts = (
    data.groupby(
        ["disposal_cohort", "allowance_group", "disposal_type"],
        observed=True
    )
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

counts.columns.name = None

# Rename count columns
counts = counts.rename(columns={
    "issued": "issued_ct",
    "abandoned": "abandoned_ct"
})

# Ensure both disposal types exist
for col in ["issued_ct", "abandoned_ct"]:
    if col not in counts.columns:
        counts[col] = 0

# Total counts
counts["total_ct"] = (
    counts["issued_ct"] + counts["abandoned_ct"]
)

# Percentages
counts["issued_pct"] = (
    counts["issued_ct"] / counts["total_ct"] * 100
).round(2)

counts["abandoned_pct"] = (
    counts["abandoned_ct"] / counts["total_ct"] * 100
).round(2)

# Clean cohort range
counts["disposal_cohort"] = (
    counts["disposal_cohort"].astype("Int64")
)

counts = Clean.remove_outsiderange(
    counts, "disposal_cohort", 1980, 2016
)

# Sort
counts = counts.sort_values(
    ["disposal_cohort", "allowance_group"]
)

# Export
counts.to_csv(
    DERIVED_DIR / "mart_disposalcounts_byallowancegrp.csv",
    index=False
)

print(counts.to_string(index=False))


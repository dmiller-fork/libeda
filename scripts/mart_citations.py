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

# Load citations
citations = pd.read_csv(
    STAGED_DIR / "stg_citations.csv",
    usecols=["app_id"],
    dtype={"app_id": "string"},
    low_memory=False
)

# Aggregate citations by application
citation_counts = (
    citations.groupby("app_id")
    .size()
    .reset_index(name="citation_count")
    .rename(columns={"app_id": "application_number"})
)

# Join
data = bins.merge(
    citation_counts,
    on="application_number",
    how="inner"
)

# Replace missing citation counts with zero
data["citation_count"] = data["citation_count"].fillna(0)

# Aggregate
counts = (
    data.groupby(
        ["disposal_cohort"],
        observed=True
    )
    .agg(
        citations_mean=("citation_count", "mean"),
        citations_median=("citation_count", "median"),
        citations_std=("citation_count", "std"),
        total_ct=("citation_count", "count")
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

print(counts.to_string(index=False))

counts.to_csv(
    DERIVED_DIR / "mart_citations.csv",
    index=False
)

# Coverage by disposal cohort
coverage = (
    data.assign(
        has_citation=data["citation_count"] > 0
    )
    .groupby("disposal_cohort", observed=True)
    .agg(
        total_apps=("application_number", "count"),
        apps_with_citations=("has_citation", "sum")
    )
    .reset_index()
)

coverage["coverage_pct"] = (
    coverage["apps_with_citations"]
    / coverage["total_apps"] * 100
)

print(coverage.to_string(index=False))

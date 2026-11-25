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
		"allowance_rate",
		"allowance_group"
	],
	dtype={"application_number": "string"},
	low_memory=False
)

# Load disposal data
disposal = pd.read_csv(
	DERIVED_DIR / "int_disposaldata_appdata.csv",
	usecols=[
		"application_number",
		"days_to_disposal"
	],
	dtype={"application_number": "string"},
	low_memory=False
)

print(f"Initial applications: {bins['application_number'].nunique():,}")

data = bins.merge(
    disposal,
    on="application_number",
    how="inner"
)

print(f"After disposal join: {data['application_number'].nunique():,}")

print("Duplicate bin IDs:", bins["application_number"].duplicated().sum())
print("Duplicate disposal IDs:", disposal["application_number"].duplicated().sum())

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

# Second join
data = data.merge(
    citation_counts,
    on="application_number",
    how="inner"
)

print(f"After citations join: {data['application_number'].nunique():,}")

# Load 892 citations
citations = pd.read_csv(
    STAGED_DIR / "stg_citations.csv",
    usecols=["app_id", "form892"],
    dtype={
        "app_id": "string",
        "form892": "Int64"
    },
    low_memory=False
)

# Filter 892 citations
citations = citations[
    citations["form892"] == 1
]

# Aggregate citations by application
citation_counts = (
    citations.groupby("app_id")
    .size()
    .reset_index(name="form892_citation_count")
    .rename(columns={"app_id": "application_number"})
)

# Third join
data = data.merge(
    citation_counts,
    on="application_number",
    how="inner"
)

print(f"After Form 892 join: {data['application_number'].nunique():,}")

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

# Fourth join
data = data.merge(
    office_action_counts,
    on="application_number",
    how="inner"
)

print(f"After office actions join: {data['application_number'].nunique():,}")

data.to_csv(
    DERIVED_DIR / "mart_join_all.csv",
    index=False
)

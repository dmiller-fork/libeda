import pandas as pd
from scipy.stats import pearsonr
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DERIVED_DIR = DATA_DIR / "derived"

allowance_df = pd.read_csv(
	DERIVED_DIR / "int_allowancerate_appdata.csv",
	dtype={"application_number": "string"}
)

disposal_df = pd.read_csv(
	DERIVED_DIR / "int_daystodisposal_appdata.csv",
	dtype={"application_number": "string"}
)

df = allowance_df.merge(
	disposal_df,
	on="application_number",
	how="inner"
)

before = len(df)
print(f"Observations Start: {before}")
df = df.dropna(subset=["days_to_disposal", "allowance_rate"])

print(f"Removed: {before - len(df)}")
print(f"Remaining: {len(df)}")
r, p = pearsonr(
	df["days_to_disposal"],
	df["allowance_rate"]
)

print(f"Pearson correlation: {r:.4f}")
print(f"P-value: {p:.3e}")

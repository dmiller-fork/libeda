import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DERIVED_DIR = DATA_DIR / "derived"

def min_independent_claim_words(df: pd.DataFrame) -> pd.DataFrame:
    independent = df[df["ind_flg"] == 1].copy()
    independent["word_ct"] = pd.to_numeric(
        independent["word_ct"], errors="coerce"
    )
    return (
        independent.groupby("appl_id", as_index=False)["word_ct"]
        .min()
        .rename(columns={"word_ct": "min_independent_claim_words"})
    )

df = pd.read_csv(RAW_DIR / "pgpub_claims_stats.csv", low_memory=False)
result = min_independent_claim_words(df)
result.to_csv(DERIVED_DIR / "min_independent_claim_words.csv", index=False)

print(result["min_independent_claim_words"].describe())

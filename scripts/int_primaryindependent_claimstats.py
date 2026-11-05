import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def min_independent_claim_words(df: pd.DataFrame) -> pd.DataFrame:
    independent = df.loc[df["ind_flg"] == 1, ["appl_id", "word_ct"]].copy()
    independent["word_ct"] = pd.to_numeric(independent["word_ct"], errors="coerce")
    return (
        independent.groupby("appl_id", as_index=False)["word_ct"]
        .min()
    )

df = pd.read_csv(STAGED_DIR / "stg_claimstats.csv", low_memory=False)
result = min_independent_claim_words(df)
result.to_csv(DERIVED_DIR / "int_primaryindependent_claimstats.csv", index=False)

## print(result["min_independent_claim_words"].describe())

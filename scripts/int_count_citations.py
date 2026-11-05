import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def count_citations(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("app_id")["citation_pat_pgpub_id"]
        .nunique()
        .reset_index(name="count")
    )


df = pd.read_csv(STAGED_DIR / "stg_citations.csv", low_memory=False)
result = count_citations(df)
result.to_csv(DERIVED_DIR / "int_count_citations.csv", index=False)

## print(result["min_independent_claim_words"].describe())

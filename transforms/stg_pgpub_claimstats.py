import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

df = pd.read_csv(RAW_DIR / "pgpub_claims_stats.csv", low_memory=False)
df.to_csv(DERIVED_DIR / "claims.csv", index=False)
DERIVED_DIR = DATA_DIR / "derived"

df = pd.read_csv(RAW_DIR / "pgpub_claims_stats.csv", low_memory=False)
df.to_csv(STAGED_DIR / "stg_pubpub_claimstats.csv", index=False)

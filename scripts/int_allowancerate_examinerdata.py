import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
DERIVED_DIR = DATA_DIR / "derived"

def allowance_rate(examiner_df: pd.DataFrame) -> pd.DataFrame:
    return examiner_df.assign(
        allowance_rate=examiner_df["issue_ct"] / examiner_df["total_ct"]
    )[["examiner_id", "allowance_rate"]]

def allowance_group(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        allowance_group=pd.cut(
            df["allowance_rate"],
            bins=[i / 10 for i in range(11)],
            right=False,
            labels=[
                f"{i}-{i+9}.99"
                for i in range(0, 100, 10)
            ]
        )
    )

examinerdata = pd.read_csv(
		DERIVED_DIR / "int_examinerid_appdata.csv",
		low_memory=False,
		dtype={"examiner_id": "string"}
	)
assert examinerdata["examiner_id"].is_unique, "Duplicate examiner_id values detected"
result = allowance_rate(examinerdata)
result = allowance_group(result)
result.to_csv(DERIVED_DIR / "int_allowancerate_examinerdata.csv", index=False)

print(result["allowance_rate"].describe())
print(result["allowance_group"].describe())

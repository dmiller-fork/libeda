import pandas as pd

def lookup(
    df: pd.DataFrame,
    key: str,
    value
) -> pd.DataFrame:

    return df[df[key] == value].copy()

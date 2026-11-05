import pandas as pd

class Transform:
	@staticmethod
	def lookup(
		df: pd.DataFrame,
		key: str,
		value
	) -> pd.DataFrame:
		return df[df[key] == value].copy()

class Analysis:
	@staticmethod
	def count_rows(df):
		"""Return the number of rows in a DataFrame."""
		return len(df)

class Clean:
	@staticmethod
	def remove_null(df, key):
		return df.dropna(subset=[key]).copy()
	@staticmethod
	def remove_negative(df, key):
		return df[df[key] >= 0].copy()

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import PercentFormatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"

df = pd.read_csv(DERIVED_DIR / "int_allowancerate_examinerdata.csv")

df = df.dropna(subset=["allowance_rate"])

plt.hist(
	df["allowance_rate"],
	bins=[i / 10 for i in range(11)],
	edgecolor="black"
)

plt.xlabel("Allowance Rate")
plt.ylabel("Number of Applications")
plt.ylabel("Number of Examiners")
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.xticks([i / 10 for i in range(11)])
plt.tight_layout()
plt.show()

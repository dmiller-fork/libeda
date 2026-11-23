import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from libeda import Analysis

x = [3000, 5000, 12000, 2000, 7000, 15000, 5000, 6000, 8000, 10000 ]  # X 
y = [7000, 8000, 25000, 5000, 12000, 30000, 10000, 15000, 20000, 18000 ]  # Y 

result = Analysis.correlation_coef(x, y)

print("Pearson correlation:", result.statistic)


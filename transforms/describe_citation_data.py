import pandas as pd

df = pd.read_csv("./citations.csv", low_memory=False)

# Count citation records per application
#citations_per_app = df.groupby("app_id").size()
citations_per_app = (
    df.groupby("app_id")["citation_pat_pgpub_id"].nunique()
)
# Descriptive statistics
print(citations_per_app.describe())

# Save application-level counts
citations_per_app.rename("citation_count").to_csv(
    "./csv/citations_per_application.csv"
)


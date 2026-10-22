from pathlib import Path

def list_datasets(directories):
    datasets = []

    for directory in directories:
        datasets.extend(Path(directory).glob("*.csv"))

    datasets = sorted(f for f in datasets if f.is_file())

    for i, dataset in enumerate(datasets, start=1):
        print(f"{i}. {dataset}")

import shutil
from pathlib import Path

import kagglehub
import pandas as pd

DATASET = "austinreese/craigslist-carstrucks-data"
RAW_DIR = Path("data/raw")
SAMPLE_DIR = Path("data/sample")


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    # Download from Kaggle (cached by kagglehub)
    path = Path(kagglehub.dataset_download(DATASET))
    print("Downloaded to:", path)
    print("Files:", [f.name for f in path.iterdir()])

    # Copy the CSV into data/raw (this folder is git-ignored)
    csv_files = list(path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV found in the downloaded dataset.")
    target = RAW_DIR / "vehicles.csv"
    shutil.copy(csv_files[0], target)

    # Print shape and save a small sample that CAN be committed to GitHub
    df = pd.read_csv(target)
    print("Shape (rows, columns):", df.shape)
    df.sample(5000, random_state=42).to_csv(SAMPLE_DIR / "vehicles_sample.csv", index=False)
    print("Sample saved to", SAMPLE_DIR / "vehicles_sample.csv")


if __name__ == "__main__":
    main()
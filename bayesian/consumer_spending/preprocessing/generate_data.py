import pandas as pd
import numpy as np
import os
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET")

s3 = boto3.client("s3", region_name=region)

np.random.seed(42)

def generate_synthetic_data(file_path):
    n = 1000
    df = pd.DataFrame({
        "Age": np.random.randint(18, 70, size=n),
        "Income": np.random.normal(60000, 15000, size=n),
        "Spending": np.random.normal(2000, 500, size=n),
        "Category": np.random.choice(["Groceries", "Travel", "Healthcare", "Electronics"], size=n)
    })

    df["Score"] = (0.3 * df["Age"] + 0.5 * df["Income"]/1000 + 0.2 * df["Spending"]/100) + np.random.normal(0, 2, size=n)
    df.to_csv(file_path, index=False)
    print(f"✅ Synthetic data saved to {file_path}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    generate_synthetic_data("data/synthetic_spending.csv")
    LOCAL_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "synthetic_spending.csv"
    S3_KEY = "data/train/synthetic_spending.csv"

    s3.upload_file(str(LOCAL_FILE), s3_bucket, S3_KEY)
    print(f"✅ Uploaded {LOCAL_FILE.name} to s3://{s3_bucket}/{S3_KEY}")

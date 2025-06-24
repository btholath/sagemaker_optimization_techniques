import os
import boto3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("S3_BUCKET")
LOCAL_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "synthetic_spending.csv"
S3_KEY = "data/train/synthetic_spending.csv"

s3 = boto3.client("s3", region_name=REGION)
s3.upload_file(str(LOCAL_FILE), BUCKET, S3_KEY)
print(f"✅ Uploaded to s3://{BUCKET}/{S3_KEY}")

import os
import boto3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("S3_BUCKET")
LOCAL_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "synthetic_spending.csv"

s3_client = boto3.client("s3", region_name=REGION)
s3_resource = boto3.resource("s3", region_name=REGION)

# Upload to 'train/' using client
s3_key_train = "data/train/synthetic_spending.csv"
s3_client.upload_file(str(LOCAL_FILE), BUCKET, s3_key_train)
print(f"✅ Uploaded to s3://{BUCKET}/{s3_key_train}")

# Upload to 'validation/' using resource
s3_key_val = "data/validation/synthetic_spending.csv"
s3_resource.Bucket(BUCKET).upload_file(str(LOCAL_FILE), s3_key_val)
print(f"✅ Uploaded to s3://{BUCKET}/{s3_key_val}")

# resource_cleanup/delete_resources.py
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET")

s3 = boto3.resource("s3", region_name=region)

# Delete all files and bucket
bucket = s3.Bucket(s3_bucket)

def cleanup_bucket():
    print(f"⚠️ Deleting contents of bucket: {s3_bucket}")
    bucket.objects.all().delete()
    bucket.delete()
    print(f"✅ Deleted bucket: {s3_bucket}")

if __name__ == "__main__":
    cleanup_bucket()
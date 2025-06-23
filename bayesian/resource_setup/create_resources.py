# resource_setup/create_resources.py
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET")
role_arn = os.getenv("ROLE_ARN")

s3 = boto3.client("s3", region_name=region)

# Create S3 bucket if not exists
def create_s3_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ S3 bucket '{bucket_name}' already exists.")
    except:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"✅ Created S3 bucket: {bucket_name}")


if __name__ == "__main__":
    create_s3_bucket(s3_bucket)
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import shutil

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
PREFIX = "data/"
ROLE_ARN = os.getenv("ROLE_ARN")
LOCAL_OUTPUT = Path(__file__).resolve().parents[2] / "output"

# AWS clients
s3 = boto3.client("s3", region_name=REGION)
sm = boto3.client("sagemaker", region_name=REGION)

def delete_s3_objects():
    logging.info(f"🧹 Deleting objects from S3 bucket: {S3_BUCKET}/{PREFIX}")
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=PREFIX)
    if "Contents" in response:
        for obj in response["Contents"]:
            logging.info(f"🗑️ Deleting {obj['Key']}")
            s3.delete_object(Bucket=S3_BUCKET, Key=obj["Key"])
    else:
        logging.info("✅ No objects found in bucket.")

def delete_sagemaker_resources():
    logging.info("🧹 Deleting SageMaker endpoint, config, and model (if exist)...")
    for name_type in ["endpoint", "endpoint-config", "model"]:
        try:
            response = sm.list_endpoints(MaxResults=1)
            if response["Endpoints"]:
                latest = response["Endpoints"][0]["EndpointName"]
                logging.info(f"🗑️ Deleting {name_type}: {latest}")
                if name_type == "endpoint":
                    sm.delete_endpoint(EndpointName=latest)
                elif name_type == "endpoint-config":
                    sm.delete_endpoint_config(EndpointConfigName=latest)
                elif name_type == "model":
                    sm.delete_model(ModelName=latest)
        except Exception as e:
            logging.warning(f"⚠️ Could not delete {name_type}: {e}")

def delete_local_output():
    if LOCAL_OUTPUT.exists():
        logging.info(f"🧹 Deleting local output directory: {LOCAL_OUTPUT}")
        shutil.rmtree(LOCAL_OUTPUT)
    else:
        logging.info("✅ No local output directory found.")

if __name__ == "__main__":
    delete_s3_objects()
    delete_sagemaker_resources()
    delete_local_output()
    logging.info("✅ Cleanup complete.")

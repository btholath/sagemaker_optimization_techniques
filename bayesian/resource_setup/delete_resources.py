import boto3
import os
import logging
import shutil
import argparse
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Constants
REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
ROLE_ARN = os.getenv("ROLE_ARN")
PREFIX = "data/"
PROJECT_TAG = "sagemaker-xgboost"  # Project-specific prefix to match SageMaker resources
LOCAL_OUTPUT = Path(__file__).resolve().parents[2] / "output"

# AWS clients
s3 = boto3.client("s3", region_name=REGION)
sm = boto3.client("sagemaker", region_name=REGION)


def delete_s3_objects(dry_run=False):
    logging.info(f"🧹 Deleting S3 objects from bucket: {S3_BUCKET}/{PREFIX}")
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=PREFIX)
    if "Contents" in response:
        for obj in response["Contents"]:
            logging.info(f"🗑️ Deleting {obj['Key']}")
            if not dry_run:
                s3.delete_object(Bucket=S3_BUCKET, Key=obj["Key"])
    else:
        logging.info("✅ No objects found in bucket.")


def delete_sagemaker_resources(dry_run=False):
    logging.info("🧹 Deleting SageMaker endpoints, models, configs, and tuning jobs")

    # Delete endpoints
    endpoints = sm.list_endpoints(NameContains=PROJECT_TAG)["Endpoints"]
    for ep in endpoints:
        name = ep["EndpointName"]
        logging.info(f"🗑️ Deleting endpoint: {name}")
        if not dry_run:
            sm.delete_endpoint(EndpointName=name)

    # Delete endpoint configs
    configs = sm.list_endpoint_configs(NameContains=PROJECT_TAG)["EndpointConfigs"]
    for cfg in configs:
        name = cfg["EndpointConfigName"]
        logging.info(f"🗑️ Deleting endpoint config: {name}")
        if not dry_run:
            sm.delete_endpoint_config(EndpointConfigName=name)

    # Delete models
    models = sm.list_models(NameContains=PROJECT_TAG)["Models"]
    for model in models:
        name = model["ModelName"]
        logging.info(f"🗑️ Deleting model: {name}")
        if not dry_run:
            sm.delete_model(ModelName=name)

    # Stop and delete tuning jobs
    jobs = sm.list_hyper_parameter_tuning_jobs(NameContains=PROJECT_TAG)["HyperParameterTuningJobSummaries"]
    for job in jobs:
        name = job["HyperParameterTuningJobName"]
        status = job["HyperParameterTuningJobStatus"]
        logging.info(f"🛑 Stopping tuning job: {name} (status: {status})")
        if status not in ["Completed", "Failed", "Stopped"] and not dry_run:
            try:
                sm.stop_hyper_parameter_tuning_job(HyperParameterTuningJobName=name)
            except Exception as e:
                logging.warning(f"⚠️ Could not stop tuning job {name}: {e}")
        if not dry_run:
            sm.delete_hyper_parameter_tuning_job(HyperParameterTuningJobName=name)

    # Delete related training jobs
    training_jobs = sm.list_training_jobs(NameContains=PROJECT_TAG)["TrainingJobSummaries"]
    for job in training_jobs:
        name = job["TrainingJobName"]
        logging.info(f"🧽 Deleting training job: {name}")
        if not dry_run:
            try:
                sm.stop_training_job(TrainingJobName=name)
            except Exception:
                pass
            try:
                sm.delete_training_job(TrainingJobName=name)
            except Exception:
                pass

    logging.info("✅ SageMaker cleanup complete.")


def delete_local_output(dry_run=False):
    if LOCAL_OUTPUT.exists():
        logging.info(f"🧹 Deleting local output directory: {LOCAL_OUTPUT}")
        if not dry_run:
            shutil.rmtree(LOCAL_OUTPUT)
    else:
        logging.info("✅ No local output directory found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup AWS SageMaker project resources")
    parser.add_argument("--dry-run", action="store_true", help="Run in test mode without actual deletions")
    args = parser.parse_args()

    delete_s3_objects(dry_run=args.dry_run)
    delete_sagemaker_resources(dry_run=args.dry_run)
    delete_local_output(dry_run=args.dry_run)

    logging.info("✅ Cleanup complete.")
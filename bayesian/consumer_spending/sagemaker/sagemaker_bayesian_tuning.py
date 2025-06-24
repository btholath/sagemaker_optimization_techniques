# bayesian/consumer_spending/sagemaker/sagemaker_bayesian_tuning.py

import os
import logging
from dotenv import load_dotenv
from pathlib import Path

import boto3
import sagemaker
from sagemaker.tuner import HyperparameterTuner, IntegerParameter, ContinuousParameter
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker import image_uris

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from project root
ROOT_DIR = Path(__file__).resolve().parents[3]
print("ROOT_DIR=", ROOT_DIR)
load_dotenv(dotenv_path=ROOT_DIR / ".env")

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
ROLE_ARN = os.getenv("ROLE_ARN")

if not all([AWS_REGION, S3_BUCKET, ROLE_ARN]):
    raise EnvironmentError("❌ Missing required environment variables in .env")

# Initialize SageMaker sessions
boto_session = boto3.Session(region_name=AWS_REGION)
sagemaker_session = sagemaker.Session(boto_session=boto_session)

# XGBoost image URI
image_uri = image_uris.retrieve("xgboost", region=AWS_REGION, version="1.3-1")

# Output location in S3
output_path = f"s3://{S3_BUCKET}/output"

# Estimator definition
estimator = Estimator(
    image_uri=image_uri,
    role=ROLE_ARN,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    volume_size=5,
    max_run=300,
    output_path=output_path,
    sagemaker_session=sagemaker_session,
    hyperparameters={
        "objective": "reg:squarederror",  # ✅ REQUIRED
        "num_round": 100                  # ✅ REQUIRED
    }
)

# Hyperparameter search space
hyperparameter_ranges = {
    "eta": ContinuousParameter(0.01, 0.3),
    "max_depth": IntegerParameter(3, 10)
}

# Hyperparameter tuner
tuner = HyperparameterTuner(
    estimator,
    objective_metric_name="validation:rmse",
    hyperparameter_ranges=hyperparameter_ranges,
    objective_type="Minimize",
    max_jobs=10,
    max_parallel_jobs=2
)

# Train input
train_input = TrainingInput(
    f"s3://{S3_BUCKET}/data/train",
    content_type="csv"
)

logger.info("🚀 Launching SageMaker Hyperparameter Tuning Job...")
tuner.fit({"train": train_input})

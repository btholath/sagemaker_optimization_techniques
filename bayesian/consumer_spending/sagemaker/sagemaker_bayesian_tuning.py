import sagemaker
from sagemaker.tuner import HyperparameterTuner, IntegerParameter, ContinuousParameter
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator

import os
from dotenv import load_dotenv
import boto3
import sagemaker

load_dotenv()
region = os.getenv("AWS_REGION")

boto_session = boto3.Session(region_name=region)
sagemaker_session = sagemaker.Session(boto_session=boto_session)

session = sagemaker.Session()
role = "arn:aws:iam::637423309379:role/SageMakerExecutionRole"

estimator = Estimator(
    image_uri="637423309379.dkr.ecr.us-east-1.amazonaws.com/xgboost:1.2-1",
    role=role,
    instance_count=1,
    instance_type='ml.m5.xlarge',
    output_path=f"s3://btholath-sagemaker-bucket/output",
    sagemaker_session=session
)

hyperparameter_ranges = {
    "max_depth": IntegerParameter(3, 10),
    "eta": ContinuousParameter(0.01, 0.3)
}

tuner = HyperparameterTuner(
    estimator,
    objective_metric_name="validation:rmse",
    hyperparameter_ranges=hyperparameter_ranges,
    objective_type="Minimize",
    max_jobs=10,
    max_parallel_jobs=2
)

tuner.fit({"train": TrainingInput("s3://btholath-sagemaker-bucket/data/train", content_type="csv")})

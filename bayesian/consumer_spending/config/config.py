import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("old BASE_DIR=", BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
print("old BASE_DIR=", BASE_DIR)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR  / "data"
OUTPUT_DIR = BASE_DIR / "output"
print("BASE_DIR=", BASE_DIR)
print("DATA_DIR=", DATA_DIR)
print("OUTPUT_DIR=", OUTPUT_DIR)
VIS_DIR = os.path.join(BASE_DIR, "visualization")
print("VIS_DIR=", VIS_DIR)


DATA_PATH = DATA_DIR / "synthetic_spending.csv"
RESULT_FILE = OUTPUT_DIR / "optimization_result.pkl"
CONVERGENCE_PLOT = OUTPUT_DIR / "convergence.png"

# Environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "btholath-default-bucket")
ROLE_ARN = os.getenv("ROLE_ARN", "arn:aws:iam::637423309379:role/SageMakerExecutionRole")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

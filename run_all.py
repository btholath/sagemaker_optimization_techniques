import os
import subprocess
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).resolve().parent / "bayesian"

# Scripts to run sequentially
scripts = [
    "resource_setup/create_resources.py",
    "consumer_spending/preprocessing/generate_data.py",
    "consumer_spending/preprocessing/upload_to_s3.py",
    "consumer_spending/tuning/bayesian_optimization.py",
    "consumer_spending/sagemaker/sagemaker_bayesian_tuning.py",
    "consumer_spending/visualization/plot_convergence.py",
]

def run_script(script):
    full_path = BASE_PATH / script
    logger.info("▶️ Running: %s", full_path)
    result = subprocess.run(["python", str(full_path)], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        logger.warning("⚠️ %s stderr:\n%s", Path(script).name, result.stderr.strip())
    logger.info("-" * 60)

if __name__ == "__main__":
    logger.info("🚀 Starting end-to-end execution of the Bayesian SageMaker pipeline...")

    for script in scripts:
        run_script(script)

    logger.info("✅ All steps completed successfully!")

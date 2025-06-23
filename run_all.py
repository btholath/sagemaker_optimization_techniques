import subprocess
import logging
import os
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR / "bayesian" / "consumer_spending"

SCRIPTS = [
    BASE_DIR / "bayesian/resource_setup/create_resources.py",
    PROJECT_ROOT / "preprocessing/generate_data.py",
    PROJECT_ROOT / "tuning/bayesian_optimization.py",
    PROJECT_ROOT / "sagemaker/sagemaker_bayesian_tuning.py",
    PROJECT_ROOT / "visualization/plot_convergence.py"
]

def run_script(script_path):
    logging.info(f"▶️ Running: {script_path}")
    result = subprocess.run(["python", str(script_path)], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        logging.warning(f"⚠️ {script_path.name} stderr:\n{result.stderr}")
    logging.info("-" * 60)

if __name__ == "__main__":
    logging.info("🚀 Starting end-to-end execution of the Bayesian SageMaker pipeline...\n")
    for script in SCRIPTS:
        run_script(script)
    logging.info("✅ All steps completed successfully!")

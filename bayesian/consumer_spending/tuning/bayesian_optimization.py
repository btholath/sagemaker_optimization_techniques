# consumer_spending/tuning/bayesian_optimization.py

from skopt.space import Real, Integer
from skopt import gp_minimize
import joblib
import numpy as np
import logging
import os
from pathlib import Path
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s"
)

# Add training module path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "preprocessing" / "synthetic_spending.csv"
RESULT_PATH = BASE_DIR.parent / "optimization_result.pkl"
PLOT_PATH = BASE_DIR / "visualization" / "convergence.png"

import sys
sys.path.append(str(BASE_DIR))
from training.train_model import train_model

def objective(params):
    learning_rate, max_depth = params
    return train_model(str(DATA_PATH), {
        "learning_rate": learning_rate,
        "max_depth": int(max_depth),
        "n_estimators": 100
    })

space = [
    Real(0.01, 0.3, name='learning_rate'),
    Integer(3, 10, name='max_depth')
]

if __name__ == "__main__":
    logging.info("🔍 Starting Bayesian Optimization...")
    result = gp_minimize(objective, space, n_calls=20, random_state=42)

    # Save result
    joblib.dump(result, RESULT_PATH)
    logging.info(f"✅ Optimization result saved to {RESULT_PATH}")
    logging.info(f"✅ Best RMSE: {result.fun:.4f} with params: {result.x}")

    # Save convergence plot
    plt.plot(result.func_vals)
    plt.title("Convergence of Bayesian Optimization")
    plt.xlabel("Iteration")
    plt.ylabel("RMSE")
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    logging.info(f"📊 Convergence plot saved to {PLOT_PATH}")

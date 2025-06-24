# bayesian_optimization.py

import sys
from pathlib import Path
import joblib
import numpy as np
from skopt import gp_minimize
from skopt.space import Real, Integer
import logging
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from bayesian.consumer_spending.training.train_model import train_model
from bayesian.consumer_spending.config.config import DATA_PATH, OUTPUT_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🔍 Starting Bayesian Optimization...")

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

result = gp_minimize(objective, space, n_calls=20, random_state=42)

output_file = OUTPUT_DIR / "optimization_result.pkl"
joblib.dump(result, output_file)
logger.info(f"✅ Bayesian Optimization completed. Result saved to {output_file}")
logger.info(f"✅ Best RMSE: {result.fun:.4f} with params: {result.x}")

# Save convergence plot
plt.plot(result.func_vals)
plt.title("Convergence of Bayesian Optimization")
plt.xlabel("Iteration")
plt.ylabel("RMSE")
plot_file = OUTPUT_DIR / "convergence.png"
plt.savefig(plot_file)
logger.info(f"✅ Convergence plot saved to {plot_file}")

# Optional: Show plot in interactive environments
try:
    plt.show()
except Exception:
    pass

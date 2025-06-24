"""
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULT_FILE = BASE_DIR / "/data" / "optimization_result.pkl"
print("BASE_DIR = ", BASE_DIR)
print("RESULT_FILE = ", RESULT_FILE)
#RESULT_FILE = "/workspaces/sagemaker_optimization_techniques/bayesian/output/optimization_result.pkl"
"""

from skopt.plots import plot_convergence
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

RESULT_FILE = Path(__file__).resolve().parent.parent.parent / "output" / "optimization_result.pkl"

try:
    result = joblib.load(RESULT_FILE)
    plot_convergence(result)
    plt.title("Convergence of Bayesian Optimization")
    plt.savefig(RESULT_FILE.parent / "convergence_reload_safe.png")
    plt.show()
except Exception as e:
    print(f"Failed to plot convergence: {e}")

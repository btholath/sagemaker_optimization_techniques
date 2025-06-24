import joblib
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULT_FILE = BASE_DIR / "/data" / "optimization_result.pkl"
print("BASE_DIR = ", BASE_DIR)
print("RESULT_FILE = ", RESULT_FILE)
RESULT_FILE = "/workspaces/sagemaker_optimization_techniques/bayesian/output/optimization_result.pkl"

result = joblib.load(RESULT_FILE)
plt.plot(result.func_vals)
plt.title("Convergence of Bayesian Optimization")
plt.xlabel("Iteration")

plt.ylabel("RMSE")
plt.savefig("visualization/convergence_plot.png")
plt.show()


from skopt.plots import plot_convergence
import matplotlib.pyplot as plt
import joblib

result = joblib.load("optimization_result.pkl")
plot_convergence(result)
plt.savefig("visualization/convergence_plot.png")

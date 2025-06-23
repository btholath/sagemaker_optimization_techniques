import pandas as pd
import numpy as np
import os

np.random.seed(42)

def generate_synthetic_data(file_path):
    n = 1000
    df = pd.DataFrame({
        "Age": np.random.randint(18, 70, size=n),
        "Income": np.random.normal(60000, 15000, size=n),
        "Spending": np.random.normal(2000, 500, size=n),
        "Category": np.random.choice(["Groceries", "Travel", "Healthcare", "Electronics"], size=n)
    })

    df["Score"] = (0.3 * df["Age"] + 0.5 * df["Income"]/1000 + 0.2 * df["Spending"]/100) + np.random.normal(0, 2, size=n)
    df.to_csv(file_path, index=False)
    print(f"✅ Synthetic data saved to {file_path}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    generate_synthetic_data("data/synthetic_spending.csv")

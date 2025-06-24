import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt

def train_model(data_path, params):
    df = pd.read_csv(data_path)
    X = df[["Age", "Income", "Spending"]]
    y = df["Score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    from math import sqrt
    #rmse = sqrt(mean_squared_error(y_test, preds))
    rmse = sqrt(mean_squared_error(y_test, preds))  # instead of passing squared=False
    print(f"validation:rmse {rmse}")  # 👈 REQUIRED for SageMaker metric extraction
    return rmse

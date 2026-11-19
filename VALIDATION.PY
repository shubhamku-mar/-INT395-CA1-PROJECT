
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
    median_absolute_error,
    explained_variance_score,
    max_error
)

# ============================================================
# 1. LOAD MODEL AND DATASET
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "demand_prediction_pipeline.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR, "LPU_Transportation_Master_Dataset_10000.xlsx"
)

if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(
        os.path.expanduser("~/Downloads"),
        "LPU_Transportation_Master_Dataset_10000 (1).xlsx"
    )

model = joblib.load(MODEL_PATH)
df = pd.read_excel(DATA_PATH, sheet_name="Ride Records")

# ============================================================
# 2. PREPARE DATA
# ============================================================
TARGET = "Passengers"

X = df.drop(
    columns=[
        TARGET,
        "Date",
        "Vehicle_Utilization_Percent",
        "Revenue_INR"
    ],
    errors="ignore"
).copy()

y = pd.to_numeric(df[TARGET], errors="coerce")

valid = y.notna()
X = X.loc[valid].reset_index(drop=True)
y = y.loc[valid].reset_index(drop=True)

# 60% train, 20% validation, 20% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.40, random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42
)

# ============================================================
# 3. EVALUATION FUNCTION
# ============================================================
def evaluate(name, X_part, y_part):
    y_pred = model.predict(X_part)

    mae = mean_absolute_error(y_part, y_pred)
    mse = mean_squared_error(y_part, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_part, y_pred)

    print(f"\n{'=' * 15} {name} {'=' * 15}")
    print(f"MAE  (Mean Absolute Error):      {mae:.6f}")
    print(f"MSE  (Mean Squared Error):       {mse:.6f}")
    print(f"RMSE (Root Mean Squared Error):  {rmse:.6f}")
    print(f"R² Score:                        {r2:.6f}")
    print(
        f"Median Absolute Error:           "
        f"{median_absolute_error(y_part, y_pred):.6f}"
    )
    print(
        f"Explained Variance Score:        "
        f"{explained_variance_score(y_part, y_pred):.6f}"
    )
    print(f"Maximum Absolute Error:          {max_error(y_part, y_pred):.6f}")

    # Percentage of predictions within passenger-count tolerances
    errors = np.abs(np.asarray(y_part) - y_pred)
    print(f"Within ±1 passenger:              {(errors <= 1).mean() * 100:.2f}%")
    print(f"Within ±2 passengers:             {(errors <= 2).mean() * 100:.2f}%")

    return y_pred


# ============================================================
# 4. RUN VALIDATION AND TEST EVALUATION
# ============================================================
print("SAVED MODEL EVALUATION")
print(f"Validation samples: {len(X_val)}")
print(f"Test samples:       {len(X_test)}")

val_pred = evaluate("VALIDATION RESULTS", X_val, y_val)
test_pred = evaluate("TEST RESULTS", X_test, y_test)

print("\nEvaluation completed.")

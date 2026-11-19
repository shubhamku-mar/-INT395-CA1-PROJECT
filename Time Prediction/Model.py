import os
import joblib
import pandas as pd
import numpy as np

# ============================================================
# 1. CONFIGURATION
# ============================================================

def get_distance_file():
    candidates = [
        "LPU_Distance_Matrix_Blocks.xlsx",
        os.path.join(os.path.dirname(__file__), "..", "LPU_Distance_Matrix_Blocks.xlsx"),
        "LPU_Distance_Matrix_Blocks.xlsx"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]

DISTANCE_FILE = get_distance_file()

OUTPUT_MODEL = "lpu_travel_time_model.pkl"
OUTPUT_DATA = "lpu_travel_time_training_data.csv"

AVERAGE_SPEED_KMPH = 17

# ============================================================
# 2. LOAD DISTANCE MATRIX
# ============================================================

print(f"Loading distance matrix from: {DISTANCE_FILE}...")

raw = pd.read_excel(
    DISTANCE_FILE,
    sheet_name="Matrix by Block ID",
    header=None
)

destination_ids = raw.iloc[3, 1:].tolist()
origin_ids = raw.iloc[4:, 0].tolist()

distance_values = raw.iloc[
    4:, 1:len(destination_ids) + 1
]

distance_matrix = pd.DataFrame(
    distance_values.to_numpy(),
    index=[str(x).strip() for x in origin_ids],
    columns=[str(x).strip() for x in destination_ids]
)

distance_matrix = distance_matrix.apply(
    pd.to_numeric, errors="coerce"
)

distance_matrix = distance_matrix.replace(
    [np.inf, -np.inf], np.nan
)

distance_matrix = distance_matrix.mask(
    distance_matrix < 0
)

# ============================================================
# 3. PROCESS DISTANCES INTO TRAVEL TIMES
# ============================================================

print("Calculating travel times at 17 km/h...")

travel_time_matrix = (
    distance_matrix * 60
    / (AVERAGE_SPEED_KMPH * 1000)
)

# ============================================================
# 4. CREATE SOURCE-DESTINATION DATASET
# ============================================================

travel_data = (
    distance_matrix
    .rename_axis(index="Source_Block", columns="Destination_Block")
    .stack()
    .rename("Distance_Meters")
    .reset_index()
)

travel_data["Distance_KM"] = (
    travel_data["Distance_Meters"] / 1000
)

travel_data["Average_Speed_KMPH"] = AVERAGE_SPEED_KMPH

travel_data["Travel_Time_Minutes"] = (
    travel_data["Distance_Meters"] * 60
    / (AVERAGE_SPEED_KMPH * 1000)
)

# ============================================================
# 5. SAVE PROCESSED DATA
# ============================================================

travel_data.to_csv(OUTPUT_DATA, index=False)

joblib.dump(
    {
        "distance_matrix": distance_matrix,
        "travel_time_matrix": travel_time_matrix,
        "average_speed_kmph": AVERAGE_SPEED_KMPH,
    },
    OUTPUT_MODEL
)

print("\nProcessing completed successfully.")
print("Source blocks:", len(distance_matrix.index))
print("Destination blocks:", len(distance_matrix.columns))
print("Valid pairs:", len(travel_data))
print("Saved data:", OUTPUT_DATA)
print("Saved reusable data:", OUTPUT_MODEL)


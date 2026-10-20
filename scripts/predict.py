import pandas as pd
import joblib

# Load trained AI model
model = joblib.load("models/bc_model.pkl")

# Load current Breeders' Cup field
df = pd.read_csv("data/horses.csv")

# Extract characteristics of all the horses for prediction

characteristics = [
    "age",
    "speedfig_avg",
    "grade1_wins",
    "speedfig_peak",
    "closer",
    "stalker",
    "frontrunner"
]

# AI predicts finish position
df["predicted_finish"] = model.predict(df[characteristics])

# Lower finish = better
df = df.sort_values("predicted_finish")

print("\n🏇 2025 Breeders' Cup Classic Prediction\n")

print(
    df[[
        "horse",
        "predicted_finish"
    ]]
)

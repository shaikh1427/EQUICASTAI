import joblib

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/training_races2.csv")

# Characterisitics of each horse
characteristics = [
    "age",
    "speedfig_avg",
    "grade1_wins",
    "speedfig_peak",
    "closer",
    "stalker",
    "frontrunner",
]


x = df[characteristics]
y = df["finish"]

# Data is split into training and testing sets, 
# with 80% for training and 20% for testing.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Builds the ai model using a random forest classifier with 100 trees 
# and a fixed random state for reproducibility.
model = RandomForestRegressor(n_estimators=500, random_state=42)

# Trains the model on the training data (training_races.csv)
# Learns patterns and relationships
model.fit(x_train, y_train)


# Now the trained model predicts where horses in the test set 
# (20% of the data) will finish in the race based on their characteristics
predictions = model.predict(x_test)

# Gets the average finish position error by comparing the predicted 
# finish positions to the actual finish positions in the test set.
mae = mean_absolute_error(
    y_test,
    predictions
)
print(f"Average Finish Position Error: {mae:.2f}")

# Calculate how spread out the model's historical prediction errors are

residuals = y_test.to_numpy() - predictions

residual_std = np.std(
    residuals,
    ddof=1
)

# measures approximately how much predictions naturally vary from reality

print(f"Simulation Error Standard Deviation: {residual_std:.2f}")


print("\nCharacteristic Importance:")

# Finds which characteristics were most influential in the results
for characteristic, importance in zip(characteristics, model.feature_importances_):

    print(f"{characteristic}: {importance:.3f}")

joblib.dump(model, "models/bc_model.pkl")

print("\nBrain Model saved successfully!")


simulation_config = {
    "characteristics": characteristics,
    "residual_std": residual_std,
    "mae": mae
}

joblib.dump(
    simulation_config,
    "models/sim_config.pkl"
)

print("\nConfiguration Model saved successfully!")

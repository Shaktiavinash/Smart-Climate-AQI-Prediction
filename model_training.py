import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import RandomForestRegressor # pyright: ignore[reportMissingModuleSource]
import joblib # type: ignore
import os

# Load sample data
df = pd.read_csv("data/historical_data.csv")  # Make sure this file exists

# Features and target
X = df[["temperature", "humidity"]]
y = df["AQI"]

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/rf_model.pkl")
print("✅ Model trained and saved as models/rf_model.pkl")

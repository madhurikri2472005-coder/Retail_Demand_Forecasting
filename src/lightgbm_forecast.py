import pandas as pd
from pathlib import Path
from lightgbm import LGBMRegressor


# Load forecasting training data
data_path = Path("data/processed/forecast_training_data.csv")

df = pd.read_csv(data_path, encoding="utf-16")

# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["sales"])

# Use one product-store combination
item_id = df["item_id"].iloc[0]
store_id = df["store_id"].iloc[0]

series = df[
    (df["item_id"] == item_id) &
    (df["store_id"] == store_id)
].copy()

# Create time-based features
series["day_number"] = range(len(series))
series["day_of_week"] = series["day_number"] % 7

# Features and target
X = series[["day_number", "day_of_week"]]
y = series["sales"]

# Train LightGBM model
model = LGBMRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=4,
    random_state=42,
    verbosity=-1
)

model.fit(X, y)

# Generate next 30 days
future_days = range(len(series), len(series) + 30)

future = pd.DataFrame({
    "day_number": future_days,
    "day_of_week": [day % 7 for day in future_days]
})

predictions = model.predict(future)

# Create forecast output
forecast = pd.DataFrame({
    "day_number": future_days,
    "predicted_sales": predictions
})

forecast["item_id"] = item_id
forecast["store_id"] = store_id

# Save forecast
output_path = Path("data/processed/lightgbm_forecast.csv")
forecast.to_csv(output_path, index=False)

print("LightGBM forecasting completed.")
print(f"Item: {item_id}")
print(f"Store: {store_id}")
print("30-day forecast generated.")
print(f"Output saved to: {output_path}")
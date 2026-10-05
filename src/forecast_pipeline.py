import pandas as pd
from pathlib import Path
from lightgbm import LGBMRegressor


# Load forecasting data
data_path = Path("data/processed/forecast_training_data.csv")
df = pd.read_csv(data_path, encoding="utf-16")

# Clean sales column
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["sales"])

# Select product-store combination
item_id = "HOBBIES_1_012"
store_id = "CA_1"

series = df[
    (df["item_id"] == item_id) &
    (df["store_id"] == store_id)
].copy()

series = series.reset_index(drop=True)

# Create time features
series["day_number"] = range(len(series))
series["day_of_week"] = series["day_number"] % 7

# Training data
X_train = series[
    ["day_number", "day_of_week"]
]

y_train = series["sales"]

# Train forecasting model
model = LGBMRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=4,
    random_state=42,
    verbosity=-1
)

model.fit(X_train, y_train)

# Generate next 30 days
future_days = range(
    len(series),
    len(series) + 30
)

future = pd.DataFrame({
    "day_number": future_days,
    "day_of_week": [
        day % 7 for day in future_days
    ]
})

# Generate predictions
predictions = model.predict(future)

# Create pipeline output
forecast = pd.DataFrame({
    "day_number": future_days,
    "predicted_sales": predictions,
    "item_id": item_id,
    "store_id": store_id
})

# Save final 30-day forecast
output_path = Path(
    "data/processed/30_day_forecast.csv"
)

forecast.to_csv(
    output_path,
    index=False
)

print("30-day forecasting pipeline completed.")
print(f"Item: {item_id}")
print(f"Store: {store_id}")
print("Forecast horizon: 30 days")
print(f"Output saved to: {output_path}")
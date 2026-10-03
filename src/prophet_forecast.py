import pandas as pd
from pathlib import Path
from prophet import Prophet


# Load forecasting training data
data_path = Path("data/processed/forecast_training_data.csv")

df = pd.read_csv(data_path, encoding="utf-16")

# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Remove invalid values
df = df.dropna(subset=["sales"])

# Use one product-store combination for Prophet
item_id = df["item_id"].iloc[0]
store_id = df["store_id"].iloc[0]

series = df[
    (df["item_id"] == item_id) &
    (df["store_id"] == store_id)
].copy()

# Convert day column to sequential dates
series["ds"] = pd.date_range(
    start="2016-01-01",
    periods=len(series),
    freq="D"
)

series["y"] = series["sales"]

# Prophet model
model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=False
)

model.fit(series[["ds", "y"]])

# Forecast next 30 days
future = model.make_future_dataframe(periods=30)

forecast = model.predict(future)

# Keep forecast results
forecast_output = forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].tail(30)

# Add product and store information
forecast_output["item_id"] = item_id
forecast_output["store_id"] = store_id

# Save forecast
output_path = Path("data/processed/prophet_forecast.csv")
forecast_output.to_csv(output_path, index=False)

print("Prophet forecasting completed.")
print(f"Item: {item_id}")
print(f"Store: {store_id}")
print(f"30-day forecast generated.")
print(f"Output saved to: {output_path}")
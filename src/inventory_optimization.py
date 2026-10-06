import pandas as pd
from pathlib import Path


# Load 30-day forecast
forecast_path = Path("data/processed/30_day_forecast.csv")
forecast = pd.read_csv(forecast_path)

# Make sure predicted sales are numeric
forecast["predicted_sales"] = pd.to_numeric(
    forecast["predicted_sales"],
    errors="coerce"
)

forecast = forecast.dropna(subset=["predicted_sales"])

# Inventory assumptions
# Safety stock = 20% of forecasted demand
forecast["safety_stock"] = (
    forecast["predicted_sales"] * 0.20
)

# Recommended stock = forecast + safety stock
forecast["recommended_stock"] = (
    forecast["predicted_sales"] +
    forecast["safety_stock"]
)

# Round inventory quantities
forecast["safety_stock"] = forecast["safety_stock"].round(2)
forecast["recommended_stock"] = forecast["recommended_stock"].round(2)

# Save inventory recommendations
output_path = Path(
    "data/processed/inventory_recommendations.csv"
)

forecast.to_csv(
    output_path,
    index=False
)

print("Inventory optimization completed.")
print(f"Item: {forecast['item_id'].iloc[0]}")
print(f"Store: {forecast['store_id'].iloc[0]}")
print("Safety stock rate: 20%")
print("30-day inventory recommendations generated.")
print(f"Output saved to: {output_path}")
import pandas as pd
from pathlib import Path


# Load forecasting training data
data_path = Path("data/processed/forecast_training_data.csv")

df = pd.read_csv(data_path, encoding="utf-16")
# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Remove invalid sales values
df = df.dropna(subset=["sales"])

# Calculate baseline demand
baseline = (
    df.groupby(["item_id", "store_id"], as_index=False)
      .agg(
          average_daily_sales=("sales", "mean"),
          total_sales=("sales", "sum")
      )
)

# Save baseline forecast
output_path = Path("data/processed/baseline_forecast.csv")
baseline.to_csv(output_path, index=False)

print("Baseline forecasting completed.")
print(f"Products/stores analyzed: {len(baseline)}")
print(f"Output saved to: {output_path}")
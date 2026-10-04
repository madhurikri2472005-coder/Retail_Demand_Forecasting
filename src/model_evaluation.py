import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
from lightgbm import LGBMRegressor
from prophet import Prophet
import numpy as np


# Load actual sales data
data_path = Path("data/processed/forecast_training_data.csv")
df = pd.read_csv(data_path, encoding="utf-16")

df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["sales"])

# Select the same product-store combination
item_id = "HOBBIES_1_012"
store_id = "CA_1"

series = df[
    (df["item_id"] == item_id) &
    (df["store_id"] == store_id)
].copy()

series = series.reset_index(drop=True)

# Create dates
series["ds"] = pd.date_range(
    start="2016-01-01",
    periods=len(series),
    freq="D"
)

# Hold out the last 3 days for testing
train = series.iloc[:-3].copy()
test = series.iloc[-3:].copy()

# -----------------------------
# Prophet evaluation
# -----------------------------

prophet_train = train[["ds", "sales"]].rename(
    columns={"sales": "y"}
)

prophet_model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=False
)

prophet_model.fit(prophet_train)

prophet_future = prophet_model.make_future_dataframe(
    periods=3,
    freq="D"
)

prophet_forecast = prophet_model.predict(prophet_future)

prophet_predictions = prophet_forecast[
    ["ds", "yhat"]
].tail(3)["yhat"].reset_index(drop=True)

actual = test["sales"].reset_index(drop=True)

prophet_mae = mean_absolute_error(
    actual,
    prophet_predictions
)

prophet_rmse = np.sqrt(
    mean_squared_error(
        actual,
        prophet_predictions
    )
)

# -----------------------------
# LightGBM evaluation
# -----------------------------

train["day_number"] = range(len(train))
train["day_of_week"] = train["day_number"] % 7

test["day_number"] = range(
    len(train),
    len(train) + len(test)
)

test["day_of_week"] = test["day_number"] % 7

X_train = train[
    ["day_number", "day_of_week"]
]

y_train = train["sales"]

X_test = test[
    ["day_number", "day_of_week"]
]

lightgbm_model = LGBMRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=4,
    random_state=42,
    verbosity=-1
)

lightgbm_model.fit(X_train, y_train)

lightgbm_predictions = lightgbm_model.predict(X_test)

lightgbm_mae = mean_absolute_error(
    actual,
    lightgbm_predictions
)

lightgbm_rmse = np.sqrt(
    mean_squared_error(
        actual,
        lightgbm_predictions
    )
)

# -----------------------------
# Evaluation results
# -----------------------------

results = pd.DataFrame({
    "model": ["Prophet", "LightGBM"],
    "MAE": [prophet_mae, lightgbm_mae],
    "RMSE": [prophet_rmse, lightgbm_rmse]
})

# Save results
output_path = Path(
    "data/processed/model_evaluation.csv"
)

results.to_csv(
    output_path,
    index=False
)

print("Model evaluation completed.")
print("Holdout test days:", len(test))
print(results)
print(f"Evaluation results saved to: {output_path}")
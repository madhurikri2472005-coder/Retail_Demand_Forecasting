import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Demand Forecasting & Inventory Optimization")
st.caption("Demand forecasting, stock planning and what-if analysis")

DATA_DIR = Path("data/processed")


def load_csv(filename):
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return None


# Load project outputs
forecast = load_csv("30_day_forecast.csv")
inventory = load_csv("inventory_recommendations.csv")
scenarios = load_csv("what_if_analysis.csv")
evaluation = load_csv("model_evaluation.csv")

if forecast is None:
    st.error("30-day forecast file not found. Run src/forecast_pipeline.py first.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

items = forecast["item_id"].dropna().unique().tolist()
selected_item = st.sidebar.selectbox("Select product", items)

stores = forecast.loc[
    forecast["item_id"] == selected_item, "store_id"
].dropna().unique().tolist()

selected_store = st.sidebar.selectbox("Select store", stores)

filtered_forecast = forecast[
    (forecast["item_id"] == selected_item)
    & (forecast["store_id"] == selected_store)
].copy()

# Key metrics
col1, col2, col3 = st.columns(3)

col1.metric("Forecast days", len(filtered_forecast))
col2.metric(
    "Total predicted demand",
    f"{filtered_forecast['predicted_sales'].sum():.2f}"
)
col3.metric(
    "Average daily demand",
    f"{filtered_forecast['predicted_sales'].mean():.2f}"
)

st.subheader("📈 30-Day Demand Forecast")
st.line_chart(
    filtered_forecast.set_index("day_number")["predicted_sales"]
)

st.dataframe(filtered_forecast, use_container_width=True)

# Inventory recommendations
st.subheader("📦 Inventory Recommendations")

if inventory is not None:
    filtered_inventory = inventory[
        (inventory["item_id"] == selected_item)
        & (inventory["store_id"] == selected_store)
    ]

    if not filtered_inventory.empty:
        st.dataframe(filtered_inventory, use_container_width=True)
        st.metric(
            "Total recommended stock",
            f"{filtered_inventory['recommended_stock'].sum():.2f}"
        )
else:
    st.info("Inventory recommendations file is not available.")

# What-if analysis
st.subheader("🔄 What-if Demand Analysis")

if scenarios is not None:
    available_scenarios = scenarios["scenario"].dropna().unique().tolist()
    selected_scenario = st.selectbox(
        "Choose demand scenario",
        available_scenarios
    )

    filtered_scenarios = scenarios[
        (scenarios["item_id"] == selected_item)
        & (scenarios["store_id"] == selected_store)
        & (scenarios["scenario"] == selected_scenario)
    ]

    st.dataframe(filtered_scenarios, use_container_width=True)

    if not filtered_scenarios.empty:
        st.metric(
            "Scenario recommended stock",
            f"{filtered_scenarios['scenario_recommended_stock'].sum():.2f}"
        )
else:
    st.info("What-if analysis file is not available.")

# Model evaluation
st.subheader("🤖 Model Evaluation")

if evaluation is not None:
    st.dataframe(evaluation, use_container_width=True)
else:
    st.info("Model evaluation results are not available.")

st.caption("Retail Demand Forecasting project | Built with Python and Streamlit")
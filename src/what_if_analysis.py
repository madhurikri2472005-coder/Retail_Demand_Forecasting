import pandas as pd
from pathlib import Path


# Load inventory recommendations
input_path = Path(
    "data/processed/inventory_recommendations.csv"
)

df = pd.read_csv(input_path)

# Demand scenarios
scenarios = {
    "Demand -10%": -0.10,
    "Baseline": 0.00,
    "Demand +10%": 0.10,
    "Demand +20%": 0.20
}

results = []

for scenario, change in scenarios.items():

    scenario_df = df.copy()

    # Adjust predicted demand
    scenario_df["scenario_demand"] = (
        scenario_df["predicted_sales"] * (1 + change)
    )

    # Apply 20% safety stock
    scenario_df["scenario_safety_stock"] = (
        scenario_df["scenario_demand"] * 0.20
    )

    # Calculate recommended stock
    scenario_df["scenario_recommended_stock"] = (
        scenario_df["scenario_demand"]
        + scenario_df["scenario_safety_stock"]
    )

    results.append(
        scenario_df[
            [
                "day_number",
                "item_id",
                "store_id",
                "scenario_demand",
                "scenario_safety_stock",
                "scenario_recommended_stock"
            ]
        ].assign(scenario=scenario)
    )

# Combine all scenarios
output = pd.concat(results, ignore_index=True)

# Save what-if analysis
output_path = Path(
    "data/processed/what_if_analysis.csv"
)

output.to_csv(
    output_path,
    index=False
)

print("What-if analysis completed.")
print("Scenarios: -10%, Baseline, +10%, +20%")
print("30-day scenario analysis generated.")
print(f"Output saved to: {output_path}")
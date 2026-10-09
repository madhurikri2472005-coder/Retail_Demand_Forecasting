# Retail Demand Forecasting & Inventory Optimization

## Project Overview

This project focuses on forecasting retail product demand and supporting
inventory optimization using historical sales data.

The project will cover:

- Data collection and preparation
- Data cleaning and ETL
- Data transformation and modeling
- Time-series demand forecasting
- 30-day demand prediction
- Inventory analysis
- What-if scenario analysis
- Interactive Streamlit dashboard

## Project Timeline

### Week 1
Data Architecture and ETL

### Week 2
Data Transformation and Modeling

### Week 3
Demand Forecasting

### Week 4
Dashboard, Inventory Optimization and Reporting

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit
- dbt
- Time-Series Forecasting

## Project Structure

```text
Retail_Demand_Forecasting/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
├── src/
├── models/
├── reports/
├── README.md
├── requirements.txt
└── .gitignore

## Final Deliverables

The project includes the following components:

- Historical retail sales data preparation and validation.
- Data transformation using dbt and BigQuery.
- Baseline, Prophet, and LightGBM forecasting models.
- Model evaluation using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
- A 30-day demand forecasting pipeline.
- Inventory optimization with safety stock.
- What-if demand analysis for different demand scenarios.
- An interactive Streamlit dashboard.

## Model Evaluation

The current prototype evaluates Prophet and LightGBM using a three-day holdout set for one product-store combination.

| Model | MAE | RMSE |
|---|---:|---:|
| Prophet | 1.5414 | 1.8214 |
| LightGBM | 0.7619 | 1.0169 |

These results are preliminary and are based on a small sample. They should not be interpreted as general performance across all products and stores.

## Run the Dashboard

Activate the project's virtual environment and run:

```bash
python -m streamlit run app.py
```

The dashboard displays demand forecasts, inventory recommendations, what-if scenarios, and model evaluation results.

## Limitations

- The current forecasting prototype uses a limited sample of historical sales.
- Forecast accuracy may change when trained on more data.
- Inventory recommendations are illustrative and should be validated before real-world use.

## Future Improvements

- Train and evaluate models across more products and stores.
- Use a larger historical dataset.
- Improve inventory calculations and round stock recommendations to whole units.
- Add interactive visualizations and additional model evaluation metrics.

## Conclusion

This project demonstrates an end-to-end retail demand forecasting workflow, from data preparation and modeling to inventory planning and interactive dashboard reporting.

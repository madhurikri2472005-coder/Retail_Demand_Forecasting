from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def validate_calendar():
    file_path = RAW_DATA_DIR / "calendar.csv"
    df = pd.read_csv(file_path)

    print("Calendar rows:", len(df))
    print("Calendar columns:", len(df.columns))
    print("Missing values by column:")
    print(df.isna().sum())

def validate_sell_prices():
    files = sorted(RAW_DATA_DIR.glob("sell_prices_part*.csv"))

    total_rows = 0
    total_missing = 0

    for file in files:
        df = pd.read_csv(file)
        total_rows += len(df)
        total_missing += df.isna().sum().sum()

    print("Sell prices rows:", total_rows)
    print("Sell prices missing values:", total_missing)


if __name__ == "__main__":
    validate_calendar()
    validate_sell_prices()
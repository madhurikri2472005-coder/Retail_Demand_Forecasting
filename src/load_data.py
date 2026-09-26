from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_calendar():
    """Load the M5 calendar dataset."""
    file_path = RAW_DATA_DIR / "calendar.csv"
    df = pd.read_csv(file_path)
    return df


def load_sell_prices():
    """Load the split sell-prices datasets."""
    files = sorted(RAW_DATA_DIR.glob("sell_prices_part*.csv"))

    if not files:
        raise FileNotFoundError("No sell_prices_part*.csv files found.")

    frames = [pd.read_csv(file) for file in files]
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    calendar_df = load_calendar()
    sell_prices_df = load_sell_prices()

    print("Calendar shape:", calendar_df.shape)
    print("Sell prices shape:", sell_prices_df.shape)
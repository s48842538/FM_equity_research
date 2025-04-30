import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

def generate_combined_graph(local_price_csv="cip-asx-share-prices.csv", save_folder="Graphs"):
    ticker = "CIP.AX"
    asx200_ticker = "^AXJO"

    # Read local share price data
    try:
        local_data = pd.read_csv(local_price_csv)
        local_data.columns = local_data.columns.str.strip()  # Remove extra whitespace
        local_data["Date"] = pd.to_datetime(local_data["Date"], utc=True)  # Add utc=True to avoid the warning
        local_data["Open"] = local_data["Open"].replace(r'[\$,]', '', regex=True).astype(float)  # Correct regex escape
    except Exception as e:
        print(f"[ERROR] Failed to read or process local CSV: {e}")
        return None

    # Set date range from the data
    start_date = local_data["Date"].min()
    end_date = local_data["Date"].max()

    # Fetch ASX200 index from Yahoo Finance
    print("Fetching ASX200 data from Yahoo Finance...")
    asx200 = yf.Ticker(asx200_ticker)
    asx200_prices = asx200.history(start=start_date, end=end_date, interval="1wk")['Close']

    if asx200_prices.empty:
        print("[ERROR] Failed to fetch ASX200 index data.")
        return None

    # Create plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot stock prices
    ax1.set_xlabel("Date")
    ax1.set_ylabel("CIP.AX Open Price", color="tab:blue")
    line1, = ax1.plot(local_data["Date"], local_data["Open"], color="tab:blue", label="CIP.AX Open Price")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot ASX200 index
    ax2 = ax1.twinx()
    ax2.set_ylabel("ASX200 Index", color="tab:orange")
    line2, = ax2.plot(asx200_prices.index, asx200_prices, color="tab:orange", label="ASX200 Index")
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Title and legend
    plt.title("CIP.AX Local Open Prices vs ASX200 Index")
    fig.legend([line1, line2],
               [line1.get_label(), line2.get_label()],
               loc='upper left', bbox_to_anchor=(0.1, 0.9), frameon=False)
    
    fig.tight_layout()

    # Save the figure
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, "combined_chart.png")
    plt.savefig(save_path)
    plt.close()

    print(f"Combined graph saved at: {save_path}")
    return save_path

# Run the function
if __name__ == "__main__":
    generate_combined_graph()

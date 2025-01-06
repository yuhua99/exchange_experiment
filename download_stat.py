import requests
import pandas as pd
import time

# Define constants
BASE_URL = "https://api.binance.com/api/v3/klines"
TRADE_PAIRS = [
    # "AAVE/USDT",
    # "AAVE/USDC",
    # "AAVE/BTC",
    # "AAVE/ETH",
    # "USDT/DAI",
    # "BTC/DAI",
    # "ETH/DAI",
    # "LINK/USDT",
    # "LINK/USDC",
    # "LINK/BTC",
    # "LINK/ETH",
    # "SAND/USDT",
    # "SAND/USDC",
    # "SAND/BTC",
    # "POL/USDT",
    # "POL/USDC",
    # "POL/BTC",
    # "POL/ETH",
    # "ETH/USDT",
    # "ETH/USDC",
    "ETH/BTC",
    # "USDC/USDT",
    # "BTC/USDT",
    # "BTC/USDC",
]
INTERVAL = "1s"  # 1-second interval
START_TIME = 1736145776000  # Start timestamp in milliseconds
END_TIME = 1736157536000    # End timestamp in milliseconds

# Function to fetch candlestick data
def fetch_candlestick_data(symbol, interval, start_time, end_time):
    symbol_pair = symbol.replace('/', '')
    all_data = []
    max_seconds = 1000000
    current_start = start_time

    while current_start < end_time:
        current_end = min(current_start + max_seconds, end_time)
        params = {
            "symbol": symbol_pair,
            "interval": interval,
            "startTime": current_start,
            "endTime": current_end,
            "limit": 1000  # Max limit per request
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            all_data.extend(response.json())
        else:
            print(f"Error fetching data for {symbol}: {response.text}")
            return []
        current_start = current_end

        # Avoid hitting rate limits
        time.sleep(0.2)

    return all_data

# Process each trading pair
for pair in TRADE_PAIRS:
    print(f"Fetching data for {pair}...")

    data = fetch_candlestick_data(pair, INTERVAL, START_TIME, END_TIME)

    # Save data to a CSV file
    if data:
        df = pd.DataFrame(data)
        df.columns = [
            "Open Time", "Open", "High", "Low", "Close", "Volume",
            "Close Time", "Quote Asset Volume", "Number of Trades",
            "Taker Buy Base Volume", "Taker Buy Quote Volume", "Ignore"
        ]
        symbol_pair = pair.replace('/', '')
        file_path = f"{symbol_pair}_candlestick_data.csv"
        df.to_csv(file_path, index=False)
        print(f"Saved data for {pair} to {file_path}")
    else:
        print(f"No data fetched for {pair}.")

print("Done!")


import pandas as pd

TRADE_PAIRS = [
    "USDT/DAI",
    "BTC/DAI",
    "ETH/DAI",
    "AAVE/USDT",
    "AAVE/USDC",
    "AAVE/BTC",
    "AAVE/ETH",
    "BTC/USDT",
    "BTC/USDC",
    "ETH/USDT",
    "ETH/USDC",
    "ETH/BTC",
    "LINK/USDT",
    "LINK/USDC",
    "LINK/BTC",
    "LINK/ETH",
    "POL/USDT",
    "POL/USDC",
    "POL/BTC",
    "POL/ETH",
    "SAND/USDT",
    "SAND/USDC",
    "SAND/BTC",
    "USDC/USDT",
]

def reorder_pair(symbol_a: str, symbol_b: str):
    priority = ["DAI", "USDT", "USDC", "BTC", "ETH"]
    symbols = {symbol_a, symbol_b}

    for curr in priority:
        if curr in symbols:
            return [symbol_b, curr] if symbol_a == curr else [symbol_a, curr]
    
    return [symbol_a, symbol_b]

# Function to load Binance data for a specific pair
def load_binance_data(pair: str):
    try:
        # Load the candlestick data for the specific pair
        binance_data = pd.read_csv(f"{pair}_candlestick_data.csv")
        # Convert the time columns to datetime
        binance_data['Open Time'] = pd.to_datetime(binance_data['Open Time'], unit='ms')
        binance_data['Close Time'] = pd.to_datetime(binance_data['Close Time'], unit='ms')
        return binance_data
    except FileNotFoundError:
        print(f"Data file for pair {pair} not found.")
        return None

# Function to find the closest Binance price for a given timestamp
def get_binance_price_data(timestamp, binance_data) -> float:
    if binance_data is not None:
        # Filter Binance data for the relevant time window
        filtered_data = binance_data[
            (binance_data['Open Time'] <= timestamp) &
            (binance_data['Close Time'] >= timestamp)
        ]
        if not filtered_data.empty:
            # Return the price information
            return float(filtered_data.iloc[0]['Close'])
    print("No price data found for the given timestamp.")

    return 0.0

def get_binance_price(symbol, timestamp) -> float:
    pair = f"{symbol}USDT"

    if symbol == "DAI":
        pair = "USDTDAI"
    elif symbol == "USDT":
        return 1.0

    binance_data = load_binance_data(pair)

    if binance_data is not None:
        # Filter Binance data for the relevant time window
        filtered_data = binance_data[
            (binance_data['Open Time'] <= timestamp) &
            (binance_data['Close Time'] >= timestamp)
        ]
        if not filtered_data.empty:
            # Return the price information
            price = float(filtered_data.iloc[0]['Close'])
            if symbol == "DAI":
                return 1 / price

            return price

    print("No price data found for the given timestamp.")

    return 0.0

def convert_asset(from_asset: str, to_asset: str, amount: float, timestamp) -> float:
    # print(f"Starting conversion: {amount} {from_asset} to {to_asset} at {timestamp}")
    symbol_a, symbol_b = reorder_pair(from_asset, to_asset)
    pair = f"{symbol_a}/{symbol_b}"

    if pair not in TRADE_PAIRS:
        sub_pair_a = f"{from_asset}USDT" if from_asset != "DAI" else f"USDTDAI"
        sub_pair_b = f"{to_asset}USDT" if to_asset != "DAI" else f"USDTDAI"

        a_data = load_binance_data(sub_pair_a)
        b_data = load_binance_data(sub_pair_b)

        a_price = get_binance_price_data(timestamp, a_data)
        b_price = get_binance_price_data(timestamp, b_data)

        if from_asset == "DAI":
            a_price = 1 / a_price
        if to_asset == "DAI":
            b_price = 1 / b_price

        a_value = a_price * amount

        result = float(a_value / b_price)
        return result

    data = load_binance_data(pair.replace('/', ''))
    price = get_binance_price_data(timestamp, data)

    if symbol_a == from_asset:
        return amount * price

    return amount / price

def main():
    # Load transaction data
    transaction_data = pd.read_csv("swap_tx.csv")
    transaction_data['Timestamp'] = pd.to_datetime(transaction_data['Timestamp'], unit='s')

    # Iterate through transactions and compare with Binance
    results = []
    for _, row in transaction_data.iterrows():
        from_asset = str(row['From'])
        to_asset = str(row['To'])
        amount = float(row['From_value'])
        timestamp = row['Timestamp']
        print(f"Processing transaction {from_asset} -> {to_asset}...")
        # print(f"hash: {row['Tx_hash']}")

        asset_amount = convert_asset(from_asset, to_asset, amount, timestamp)
        net_amount = float(row['To_value']) - asset_amount
        price = get_binance_price(to_asset, timestamp)

        results.append({
            "Tx hash": row['Tx_hash'],
            "From": from_asset,
            "To": to_asset,
            "Amount": row['To_value'],
            "Binance amount": asset_amount,
            "Profit": price * net_amount,
            "Profit percentage": net_amount / asset_amount
        })

    # Create a results DataFrame
    results_df = pd.DataFrame(results)

    # Save results to a CSV or display
    results_df.to_csv('price_comparison_results.csv', index=False)
    print("Price comparison completed. Results saved to 'price_comparison_results.csv'.")

main()

import pandas as pd

# Sample CSV data path
file_path = "simplified.csv"

# Sample data columns
columns = ["Transaction Hash", "UnixTimestamp", "From", "To", "TokenValue", "TokenSymbol"]

# Mock data (load your real CSV here)

# Create DataFrame from data
df = pd.read_csv(file_path, names=columns)
df['TokenSymbol'] = df['TokenSymbol'].replace('USDC.e', 'USDC')
df['TokenSymbol'] = df['TokenSymbol'].replace('WMATIC', 'POL')
df['TokenSymbol'] = df['TokenSymbol'].replace('WBTC', 'BTC')
df['TokenSymbol'] = df['TokenSymbol'].replace('WETH', 'ETH')


# Initialize an empty list to store the swap details
swap_details = []

# Group by Transaction Hash to process each transaction separately
grouped = df.groupby('Transaction Hash')

for tx_hash, group in grouped:
    # Ensure we only process rows with two distinct tokens in the same transaction
    if len(group) == 2:
        row1, row2 = group.iloc[0], group.iloc[1]
        timestamp = row1['UnixTimestamp']

        if row1['From'] == 'me':
            token_out, value_out = row1['TokenSymbol'], row1['TokenValue']
            token_in, value_in = row2['TokenSymbol'], row2['TokenValue']
        else:
            token_out, value_out = row2['TokenSymbol'], row2['TokenValue']
            token_in, value_in = row1['TokenSymbol'], row1['TokenValue']

        # Calculate the swap ratio (token_out to token_in)
        try:
            value_out = value_out.replace(',', '')
            value_in = value_in.replace(',', '')
            swap_details.append({
                "Tx_hash": tx_hash,
                "Timestamp": timestamp,
                "From": token_out,
                "From_value": value_out,
                "To": token_in,
                "To_value": value_in,
            })
        except ZeroDivisionError:
            swap_details.append({
                "Tx_hash": tx_hash,
                "Timestamp": timestamp,
                "From": token_out,
                "From_value": value_out,
                "To": token_in,
                "To_value": value_in,
            })

# Convert swap details into a DataFrame
swap_df = pd.DataFrame(swap_details)

# Save the results to a CSV file
output_path = "swap_tx.csv"
swap_df.to_csv(output_path, index=False)


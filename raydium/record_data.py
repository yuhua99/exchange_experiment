import requests
import time
import json

# URL and headers for the API request
mint_table = {
    "GOAT": "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump",
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
}
pool_table = {
    "9Tb2ohu5P16BpBarqd3N27WnkF51Ukfs8Z1GzzLDxVZW": "SOL-GOAT",
    "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2": "SOL-USDC",
    "9TsBPrmzwjicRR2pfgGYowBnm2pVHd7p6Sdm4HgneyM3": "GOAT-USDC",
}

base_url = "https://api-v3.raydium.io/pools/info"
headers = {"accept": "application/json"}

json_writers = {}


def generate_pool_info_url_by_mint(mint_a: str, mint_b: str) -> str:
    pool_type = "standard"
    pool_sort_field = "volume24h"
    sort_type = "desc"
    page_size = 1
    page = 1
    return (
        f"{base_url}/mint?mint1={mint_a}&mint2={mint_b}&poolType={pool_type}"
        f"&poolSortField={pool_sort_field}&sortType={sort_type}"
        f"&pageSize={page_size}&page={page}"
    )


def generate_pool_info_url_by_ids() -> str:
    id = "%2c".join(pool_table.keys())
    return f"{base_url}/ids?ids={id}"


def init_writers():
    for pool_id in pool_table:
        json_writers[pool_id] = open(f"{pool_table[pool_id]}_pool_info.json", "w")


def handle_data(timestamp, data):
    id = data["id"]
    writer = json_writers[id]

    processed_data = {
        "timestamp": timestamp,
        "price": data["price"],
        "feeRate": data["feeRate"],
        "tvl": data["tvl"],
    }

    if writer:
        json.dump(processed_data, writer)
        writer.write("\n")
        writer.flush()


def main():
    init_writers()
    url = generate_pool_info_url_by_ids()
    print(url)

    try:
        cur_timestamp = int(time.time())
        while True:
            start_time = time.time()  # Record the start time

            # Make the GET request
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                resp = response.json()
                datas = resp["data"]

                for data in datas:
                    handle_data(cur_timestamp, data)

            else:
                print(f"Error: Received status code {response.status_code}")

            if abs(cur_timestamp - int(time.time())) >= 3:
                print("warning: time drift detected")
                cur_timestamp = int(time.time())

            # Calculate the time taken for the request
            elapsed_time = time.time() - start_time

            # Ensure 1-second intervals
            sleep_duration = max(1 - elapsed_time, 0)
            time.sleep(sleep_duration)
            cur_timestamp += 1

    except KeyboardInterrupt:
        print("Stopped logging.")


main()

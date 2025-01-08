import websocket
import json

# API endpoint and headers
ws_url = "wss://api.hyperliquid.xyz/ws"

# Parameters
COIN = "GOAT"  # Change this to the desired coin
interval = 1  # 1 second interval


def on_message(ws, message):
    """Callback for receiving messages."""
    raw_data = json.loads(message)
    data = raw_data.get("data", {})
    timestamp = data.get("time")

    levels = data.get("levels", [])
    if len(levels) < 2:
        print(f"Error: Invalid order_book, timestamp = {timestamp}")

    row = {
        "timestamp": timestamp,
        "bids": levels[0],
        "offers": levels[1],
    }

    with open(f"{COIN}_order_book.json", "a") as f:
        json.dump(row, f)
        f.write("\n")


def on_error(ws, error):
    """Callback for handling errors."""
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    """Callback for when the WebSocket connection is closed."""
    print("WebSocket closed")


def on_open(ws):
    print("Websocket connection opened")
    request = {
        "method": "subscribe",
        "subscription": {
            "type": "l2Book",
            "coin": COIN,
        },
    }
    ws.send(json.dumps(request))


ws = websocket.WebSocketApp(
    ws_url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.on_open = on_open
ws.run_forever()

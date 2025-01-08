import websocket
import time
import json

# API endpoint and headers
ws_url = "wss://api.hyperliquid.xyz/ws"

# Parameters
coin = "GOAT"  # Change this to the desired coin
interval = 1  # 1 second interval


def on_message(ws, message):
    """Callback for receiving messages."""
    current_time = int(time.time())  # Current time in epoch seconds
    data = json.loads(message)
    mids = data.get("data", {}).get("mids", [])

    row = {"timestamp": current_time}
    row.update(mids)

    with open("hyperliquid_all_mids.json", "a") as f:
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
            "type": "allMids",
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

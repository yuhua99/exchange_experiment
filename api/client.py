import requests
from decimal import Decimal
import config
from enum import Enum

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class ClientOrder:
    def __init__(self, symbol: str, side: OrderSide, limit_price: Decimal, quantity: Decimal, post_only: bool = False, client_id: str = ""):
        self.symbol = symbol
        self.side = side
        self.limit_price = limit_price
        self.quantity = quantity
        self.post_only = post_only
        self.client_id = client_id

    def to_dict(self):
        """Convert the order to a dictionary for API submission."""
        return {
            "symbol": self.symbol,
            "side": self.side.value,
            "limit_price": str(self.limit_price),
            "quantity": str(self.quantity),
            "post_only": self.post_only,
            "client_id": self.client_id
        }

class ApiClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.api_key = config.API_KEY

    def send_order(self, order: ClientOrder):
        """Send an order to the crypto exchange."""
        url = f"{self.base_url}/orders"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        order_data = order.to_dict()

        try:
            response = requests.post(url, json=order_data, headers=headers)
            if response.status_code == 200:
                return {"status": "success", "order_id": response.json().get("order_id")}
            else:
                error_message = response.json().get("error", "Unknown error")
                return {"status": "error", "reason": error_message}
        except requests.exceptions.RequestException as e:
            # Handle any request errors (e.g., network issues)
            return {"status": "error", "reason": str(e)}


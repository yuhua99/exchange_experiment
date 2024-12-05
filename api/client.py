from decimal import Decimal
from enum import Enum
import okx.Account as Account

API_KEY = ""
SECRET_KEY = ""
PASS_PHRASE = ""
DEMO_TRADING_FLAG = "0" # 0: live trading, 1: demo trading

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

def get_balance(symbol: str, flag="1"):
    account_api = Account.AccountAPI(API_KEY, SECRET_KEY, PASS_PHRASE, False, flag)
    result = account_api.get_account_balance({"ccy": symbol})
    return result

def main():
    print("hello")
    print(get_balance("ETH", DEMO_TRADING_FLAG))

if __name__ == "__main__":
    main()

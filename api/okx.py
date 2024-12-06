from decimal import Decimal
from enum import Enum
import okx.Account as Account
import okx.PublicData as PublicData

API_KEY = ""
SECRET_KEY = ""
PASS_PHRASE = ""
DEMO_TRADING_FLAG = "0" # 0: live trading, 1: demo trading

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class ClientOrder:
    def __init__(
        self,
        symbol: str,
        side: OrderSide,
        limit_price: Decimal,
        quantity: Decimal,
        post_only: bool = False,
        client_id: str = "",
    ):
        self.symbol = symbol
        self.side = side
        self.limit_price = limit_price
        self.quantity = quantity
        self.post_only = post_only
        self.client_id = client_id


# TODO: add error handling
def _parse_balance_resp(resp: dict) -> str:
    avail_bal_str = resp['data'][0]['details'][0]['availBal']
    avail_bal = float(avail_bal_str)
    return str(avail_bal)

# TODO: support batch get balance
def get_balance(symbol: str, flag="1") -> dict:
    account_api = Account.AccountAPI(API_KEY, SECRET_KEY, PASS_PHRASE, False, flag)
    resp = account_api.get_account_balance(symbol)
    return {symbol: _parse_balance_resp(resp)}

# TODO: add error handling
def _parse_instrument_resp(resp: dict):
    price_tick_size = resp['data'][0]['minSz']
    volume_tick_size = resp['data'][0]['lotSz']

    return {
        "price_tick_size": price_tick_size,
        "volume_tick_size": volume_tick_size
    }

# Rate limit = 20 requests per 2 seconds
# TODO: support batch get balance
def get_market_stat(symbol: str, flag="1") -> dict:
    public_data_api = PublicData.PublicAPI(flag=flag)
    resp = public_data_api.get_instruments(instType="SPOT", instId=symbol)
    return {symbol: _parse_instrument_resp(resp)}

# Rate limit = 60 requests per 2 seconds
# Rate limit rule (except Options): UserID + Instrument ID
def send_order(client_order: ClientOrder) -> dict:
    return {}

def main():
    print(get_balance("ETH", DEMO_TRADING_FLAG))
    print(get_market_stat("ETH-USDT", DEMO_TRADING_FLAG))

if __name__ == "__main__":
    main()


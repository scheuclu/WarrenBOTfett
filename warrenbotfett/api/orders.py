import logfire
import requests

from warrenbotfett.common import ToolError, Trading212Ticker
from warrenbotfett.models import Order
from warrenbotfett.utils.secrets import secrets


def place_buy_order(ticker: Trading212Ticker, quantity: float) -> Order | ToolError:
    """Buying asset with specific ticker on Trading212"""

    try:
        url = "https://demo.trading212.com/api/v0/equity/orders/market"

        payload = {
            "quantity": quantity,
            "ticker": ticker.value,  # "AAPL_US_EQ"
        }

        headers = {
            "Authorization": secrets.trading212_api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return Order(**data)
    except Exception as e:
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


def place_sell_order(
    ticker: Trading212Ticker, quantity: float, stop_price: float
) -> Order | ToolError:
    """Selling an asset with specific ticker on Trading212.

    The `quantity` needs to be negative.
    """
    try:
        url = "https://demo.trading212.com/api/v0/equity/orders/stop"

        payload = {
            "quantity": quantity,  # 0.01
            "stopPrice": stop_price,  # 2960
            "ticker": ticker.value,
            "timeValidity": "DAY",
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": secrets.trading212_api_key,
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()
        return Order(**data)
    except Exception as e:
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


if __name__ == "__main__":
    # pass
    result = place_buy_order(ticker=Trading212Ticker.AAPL_US_EQ, quantity=0.1)
    # result = place_sell_order(ticker="AMZN_US_EQ", quantity=0.01, stop_price=2960.0)
    print(result)
    # place_sell_order(ticker='5SPYl_EQ', quantity=0.01, stop_price=2960.0)

import logfire
import requests

from warrenbotfett.common import ToolError, Trading212Ticker
from warrenbotfett.models import Order
from warrenbotfett.utils.secrets import secrets


def cancel_order_by_id(id: int) -> bool | ToolError:
    try:
        url = "https://demo.trading212.com/api/v0/equity/orders/" + str(id)

        headers = {
            "Authorization": secrets.trading212_api_key,
            # "Content-Type": "application/json",
        }

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.status_code == 200
    except Exception as e:
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


def fetch_open_orders() -> list[Order] | ToolError:
    try:
        url = "https://demo.trading212.com/api/v0/equity/orders"

        headers = {
            "Authorization": secrets.trading212_api_key,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return [Order(**d) for d in data]
    except Exception as e:
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


def cancel_open_orders():
    open_orders: list[Order] | ToolError = fetch_open_orders()
    assert isinstance(open_orders, list)
    for order in open_orders:
        if order.id:
            assert cancel_order_by_id(order.id)


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
    # open_orders = fetch_open_orders()
    cancel_open_orders()

    # {'strategy': 'QUANTITY', 'id': 37400305303, 'type': 'MARKET', 'ticker': 'NVDA_US_EQ', 'quantity': 1.0,
    #  'filledQuantity': 0, 'limitPrice': None, 'stopPrice': None, 'status': 'NEW',
    #  'creationTime': '2025-09-20T18:45:26.746+03:00', 'value': None, 'filledValue': None}
    # {'strategy': 'QUANTITY', 'id': 37400305301, '

    # pass
    # result = place_buy_order(ticker=Trading212Ticker.AAPL_US_EQ, quantity=0.1)
    # result = place_sell_order(ticker="AMZN_US_EQ", quantity=0.01, stop_price=2960.0)
    # print(result)
    # place_sell_order(ticker='5SPYl_EQ', quantity=0.01, stop_price=2960.0)

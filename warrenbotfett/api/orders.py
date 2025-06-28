import requests

from warrenbotfett.models import Order
from warrenbotfett.utils.secrets import secrets


def place_buy_order(ticker: str, quantity: float) -> Order:
    """Buying asset with specific ticker"""

    url = "https://demo.trading212.com/api/v0/equity/orders/market"

    payload = {
        "quantity": quantity,
        "ticker": ticker,  # "AAPL_US_EQ"
    }

    headers = {"Authorization": secrets.trading212_api_key}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    return Order(**data)


def place_sell_order(ticker: str, quantity: float, stop_price: float) -> Order:
    """Selling an asset with specific ticker

    The `quantity` needs to be negative.
    """

    url = "https://demo.trading212.com/api/v0/equity/orders/stop"

    payload = {
        "quantity": quantity,  # 0.01
        "stopPrice": stop_price,  # 2960
        "ticker": ticker,
        "timeValidity": "DAY",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": secrets.trading212_api_key,
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    return Order(**data)


if __name__ == "__main__":
    pass
    # place_buy_order(ticker="5SPYl_EQ", quantity=-0.01)
    # place_sell_order(ticker='5SPYl_EQ', quantity=0.01, stop_price=2960.0)

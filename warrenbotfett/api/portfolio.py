import requests
from dotenv import load_dotenv

from warrenbotfett.models import Position
from warrenbotfett.utils.secrets import secrets

load_dotenv()


def get_all_positions() -> list[Position]:
    """Lists all equity positions the user currently holds. E.g. the holdings of Apple stock or the holdings in ETFs"""
    url = "https://demo.trading212.com/api/v0/equity/portfolio"

    headers = {"Authorization": secrets.trading212_api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    return [Position(**d) for d in data]


# 5SPYl_EQ


def get_specific_position(
    ticker: str,
) -> Position:  # TODO: type the valid tickers. Make it
    url = "https://demo.trading212.com/api/v0/equity/portfolio/" + ticker

    headers = {"Authorization": secrets.trading212_api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    return Position(**data)


if __name__ == "__main__":
    get_all_positions()

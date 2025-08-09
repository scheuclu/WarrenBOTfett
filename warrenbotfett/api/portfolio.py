import asyncio
import time

import logfire
import requests
from dotenv import load_dotenv

from warrenbotfett.common import ToolError, Trading212Ticker
from warrenbotfett.models import Position
from warrenbotfett.utils.secrets import secrets

load_dotenv()


def get_all_positions() -> list[Position] | ToolError:
    """Lists all equity positions the user currently holds. E.g. the holdings of Apple stock or the holdings in ETFs"""
    try:
        url = "https://demo.trading212.com/api/v0/equity/portfolio"

        headers = {
            "Authorization": secrets.trading212_api_key,
            "Content-Type": "application/json",
        }

        time.sleep(5)
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return [Position(**d) for d in data]
    except Exception as e:
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


# 5SPYl_EQ

get_specific_position_lock = asyncio.Lock()
from warrenbotfett.common import ToolError


async def get_specific_position(
    ticker: Trading212Ticker,
) -> Position | ToolError:
    "Get all data about the holdings of a particular ticker on Trading212."
    async with get_specific_position_lock:
        try:
            url = "https://demo.trading212.com/api/v0/equity/portfolio/" + ticker.value

            headers = {
                "Authorization": secrets.trading212_api_key,
                "Content-Type": "application/json",
            }

            time.sleep(1)
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            # log.info(str(data))
            return Position(**data)
        except Exception as e:
            logfire.error(str(e))
            return ToolError(message=str(e), error_type="RequestError")


if __name__ == "__main__":
    get_all_positions()

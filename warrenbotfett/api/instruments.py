import logfire
import requests
from diskcache import Cache
from dotenv import load_dotenv

from warrenbotfett.common import ToolError
from warrenbotfett.models import TradeableInstrument
from warrenbotfett.utils.secrets import secrets

cache = Cache(".")  # persistent on disk


def cached(ttl_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache.set(key, result, expire=ttl_seconds)
            return result

        return wrapper

    return decorator


load_dotenv()

SUBSET_ISIN = [
    "US5949181045",
    "US0378331005",
    "US67066G1040",
    "US0231351067",
    "US02079K3059",
    "US30303M1027",
    "US0846707026",
    "US5324571083",
    "US11135F1012",
    "US46625H1005",
    "US88160R1014",
    "US92826C8394",
    "US30231G1022",
    "US4781601046",
    "US91324P1021",
    "US7427181091",
    "US57636Q1040",
    "US4370761029",
    "US22160K1051",
    "US9311421039",
]

SUBSET_TICKER = ["5SPYl_EQ"]


# @cached(ttl_seconds=3600)
def list_instruments() -> list[TradeableInstrument] | ToolError:
    try:
        url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"

        headers = {"Authorization": secrets.trading212_api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return [
            TradeableInstrument(**d)
            for d in data
            if (d["isin"] in SUBSET_ISIN or d["ticker"] in SUBSET_TICKER)
        ]
    except Exception as e:
        logfire.error(str(e))
        return ToolError(error_type="Failed to list instruments.", message=str(e))


if __name__ == "__main__":
    instruments = list_instruments()
    if not isinstance(instruments, Exception):
        for item in instruments:
            print(item)

import requests

from warrenbotfett.common import ToolError
from warrenbotfett.models import Cash
from warrenbotfett.utils.secrets import secrets


def cash() -> Cash | ToolError:
    try:
        url = "https://demo.trading212.com/api/v0/equity/account/cash"

        headers = {"Authorization": secrets.trading212_api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return Cash(**data)
    except Exception as e:
        return ToolError(message=str(e), error_type="Failed to read cash.")


if __name__ == "__main__":
    c = cash()
    print(c)

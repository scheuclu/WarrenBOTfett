import os

from dotenv import load_dotenv

from warrenbotfett.models import Secrets

load_dotenv()

trading212_api_key = os.environ.get("TRADING212_KEY", None)
if not trading212_api_key:
    raise ValueError("Environment variable `TRADING212_KEY` not set.")


secrets = Secrets(trading212_api_key=trading212_api_key)

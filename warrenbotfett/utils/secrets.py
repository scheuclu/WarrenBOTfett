import os

from dotenv import load_dotenv

from warrenbotfett.models import Secrets

load_dotenv()

trading212_api_key = os.environ.get("TRADING212_KEY", None)
if not trading212_api_key:
    raise ValueError("Environment variable `TRADING212_KEY` not set.")

supabase_url = os.environ.get("SUPABASE_URL", None)
if not supabase_url:
    raise ValueError("Environment variable `SUPABASE_URL` not set.")

supabase_key = os.environ.get("SUPABASE_KEY", None)
if not supabase_key:
    raise ValueError("Environment variable `SUPABASE_KEY` not set.")


secrets = Secrets(
    trading212_api_key=trading212_api_key,
    supabase_url=supabase_url,
    supabase_key=supabase_key,
)

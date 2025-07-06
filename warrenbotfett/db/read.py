from datetime import datetime

from supabase import Client, create_client

from warrenbotfett.common import BotSummary
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def read_summary() -> dict[datetime, BotSummary]:
    response = supabase.table("DailySummaries").select("*").execute()
    return {
        datetime.fromisoformat(d["created_at"]): BotSummary.model_validate_json(
            d["summary"]
        )
        for d in response.data
    }


if __name__ == "__main__":
    summary = read_summary()
    print(f"{summary=}")

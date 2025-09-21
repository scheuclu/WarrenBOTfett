from datetime import datetime

from supabase import Client, create_client

from warrenbotfett.common import BotSummary2
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def read_summary() -> dict[datetime, BotSummary2]:
    response = supabase.table("DailySummaries").select("*").execute()
    return {
        datetime.fromisoformat(d["created_at"]): BotSummary2.model_validate_json(
            d["summary"]
        )
        for d in response.data
    }


def read_agent_results():
    response = supabase.table("agent_results").select("*").execute()
    return response.data


def read_sp500_benchmark():
    response = supabase.table("sp500_benchmark").select("*").execute()
    return response.data


if __name__ == "__main__":
    # summary = read_summary()
    # print(f"{summary=}")
    data = read_sp500_benchmark()
    print(data)

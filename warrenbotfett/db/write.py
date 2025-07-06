from supabase import Client, create_client

from warrenbotfett.common import BotSummary, ToolCall
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def store_summary(summary: BotSummary) -> bool:
    response = (
        supabase.table("DailySummaries")
        .insert({"summary": summary.model_dump_json()})
        .execute()
    )
    return response.data is not None and len(response.data) != 0


if __name__ == "__main__":
    summary = BotSummary(
        reasoning="There is not good reason",
        tool_calls=[
            ToolCall(
                function_name="aaa", kwargs={"bb": 1}, reasoning="This was the reason"
            )
        ],
    )
    success = store_summary(summary=summary)
    print(f"{success=}")

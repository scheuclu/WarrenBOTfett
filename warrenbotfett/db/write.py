from pydantic_ai.agent import AgentRunResult
from supabase import Client, create_client

from warrenbotfett.common import BotSummary, ToolCall
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def store_summary(run_result: AgentRunResult) -> bool:
    response = (
        supabase.table("DailySummaries")
        .insert({"summary": run_result.output.model_dump_json()})
        .execute()
    )
    # run_result.all_messages_json()
    # run_result.output.model_dump_json()
    # run_result.usage().usage.__dict__
    response = (
        supabase.table("agent_results")
        .insert(
            {
                "messages": run_result.all_messages_json().decode(encoding="utf-8"),
                "output": run_result.output.model_dump_json(),
                "usage": run_result.usage().__dict__,
            }
        )
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

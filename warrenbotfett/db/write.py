from pydantic_ai.agent import AgentRunResult
from supabase import Client, create_client

from warrenbotfett.common import BotSummary, PositionAnalysis, ToolCall
from warrenbotfett.utils.secrets import secrets

supabase: Client = create_client(secrets.supabase_url, secrets.supabase_key)


def store_summary(run_result: AgentRunResult[BotSummary]) -> bool:
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
    bot_summary = BotSummary(
        position_summaries=[
            PositionAnalysis(instrument="AAPL", report="asdasdasdasdads")
        ],
        overall_summary="Overall, everything is great",
        tool_calls=[
            ToolCall(
                function_name="aaa", kwargs={"bb": 1}, reasoning="This was the reason"
            )
        ],
    )
    from pydantic_ai._agent_graph import GraphAgentState, _usage

    agent_run_result = AgentRunResult[BotSummary](
        output=bot_summary,
        _output_tool_name="None",
        _state=GraphAgentState(
            message_history=[], usage=_usage.Usage(), retries=0, run_step=0
        ),
        _new_message_index=0,
        _traceparent_value="None",
    )

    # _output_tool_name: str | None = dataclasses.field(repr=False)
    # _state: _agent_graph.GraphAgentState = dataclasses.field(repr=False)
    # _new_message_index: int = dataclasses.field(repr=False)
    # _traceparent_value: str | None = dataclasses.field(repr=False)

    success = store_summary(run_result=agent_run_result)
    print(f"{success=}")

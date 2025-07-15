from pydantic import BaseModel, Field


class ToolError(BaseModel):
    error_type: str = Field(description="Type of the error that has occured.")
    message: str = Field(description="A message describing what exactly the issue is.")


class ToolCall(BaseModel):
    function_name: str = Field(description="Name of the tool that will be called.")
    kwargs: dict = Field(
        description="Arguments that the function is being called with."
    )
    reasoning: str = Field(
        description="Reasoning behind the agent making this particular tool call."
    )


class PositionAnalysis(BaseModel):
    instrument: str = Field(
        description="Name of the instrument we have an active position in."
    )
    report: str = Field(
        description="Daily analysis of this position. This should be based on performance as well as recent news and market data."
    )


class BotSummary(BaseModel):
    position_summaries: list[PositionAnalysis] = Field(
        description="Analysis for every position we are active in"
    )
    overall_summary: str = Field(
        description="An overall summary. This should include other investments that have been considered. Even if they have not been made. We want the reasoning."
    )
    tool_calls: list[ToolCall] = Field(
        description="List of tool calls that the agent has made to make a trade. No tool calls that are just reading data."
    )

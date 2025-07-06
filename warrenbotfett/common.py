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


class BotSummary(BaseModel):
    reasoning: str = Field(
        description="a comprehensive reasonsing for the agent desscions. Regardless of whether trades have been made or not."
    )
    tool_calls: list[ToolCall] = Field(
        description="List of tool calls that the agent has made to make a trade. No tool calls that are just reading data."
    )

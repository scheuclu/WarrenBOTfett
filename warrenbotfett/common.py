from enum import Enum

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


class Trading212Ticker(Enum):
    """Ticker string used for all trading212 endpoints"""

    AAPL_US_EQ = "AAPL_US_EQ"
    MSFT_US_EQ = "MSFT_US_EQ"
    AMZN_US_EQ = "AMZN_US_EQ"
    LLY_US_EQ = "LLY_US_EQ"
    HDId_EQ = "HDId_EQ"
    THREE_V64d_EQ = "3V64d_EQ"
    FB_US_EQ = "FB_US_EQ"
    ONE_YDd_EQ = "1YDd_EQ"
    PG_US_EQ = "PG_US_EQ"
    AMZd_EQ = "AMZd_EQ"
    XONAd_EQ = "XONAd_EQ"
    CMCd_EQ = "CMCd_EQ"
    LLYd_EQ = "LLYd_EQ"
    WMT_US_EQ = "WMT_US_EQ"
    ABEAd_EQ = "ABEAd_EQ"
    GOOGL_US_EQ = "GOOGL_US_EQ"
    MA_US_EQ = "MA_US_EQ"
    WMTd_EQ = "WMTd_EQ"
    PRGd_EQ = "PRGd_EQ"
    V_US_EQ = "V_US_EQ"
    NVDd_EQ = "NVDd_EQ"
    AVGO_US_EQ = "AVGO_US_EQ"
    FB2Ad_EQ = "FB2Ad_EQ"
    CTOd_EQ = "CTOd_EQ"
    MSFd_EQ = "MSFd_EQ"
    JPM_US_EQ = "JPM_US_EQ"
    TSLA_US_EQ = "TSLA_US_EQ"
    COST_US_EQ = "COST_US_EQ"
    TL0d_EQ = "TL0d_EQ"
    XOM_US_EQ = "XOM_US_EQ"
    UNH_US_EQ = "UNH_US_EQ"
    NVDA_US_EQ = "NVDA_US_EQ"
    BRYNd_EQ = "BRYNd_EQ"
    HD_US_EQ = "HD_US_EQ"
    JNJd_EQ = "JNJd_EQ"
    BRK_B_US_EQ = "BRK_B_US_EQ"
    M4Id_EQ = "M4Id_EQ"
    UNHd_EQ = "UNHd_EQ"
    FIVE_SPYl_EQ = "5SPYl_EQ"
    APCd_EQ = "APCd_EQ"
    JNJ_US_EQ = "JNJ_US_EQ"

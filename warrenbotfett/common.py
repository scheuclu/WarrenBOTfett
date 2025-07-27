from enum import Enum, StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class ToolError(BaseModel):
    """Whenever this is returned, it means something went wront when calling a tool and we are capturing the problem here."""

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


class NewsInterpretationSentiment(StrEnum):
    POSITIVE = (
        "POSITIVE"  # = Field(description='Enum value for positive news sentiment')
    )
    NEUTRAL = "NEUTRAL"  # = Field(description='Enum value for neutral or unknown news sentiment.')
    NEGATIVE = (
        "NEGATIVE"  # = Field(description='Enum value for negative news sentiment')
    )


class NewsInterpretation(BaseModel):
    ticker: str = Field("Ticker of the company that has been analyzed")
    sentiment: NewsInterpretationSentiment = Field(
        description="A characterterization of how the general sentiment of the news articles is. If not enought data, do `NEUTRAL`. If very good select `POSITIVE` if bad, select `NEGATIVE`."
    )
    summary: str = Field(
        "Summary of the current news. Ideally around 1000 characters. If no news can Be found, put the phrase `No news found` 20 times",
        min_length=0,
        max_length=2000,
    )


class NewsPiece(BaseModel):
    title: str
    content: str | None = None


class RawNewsInformation(BaseModel):
    ticker: str = Field("Name of the ticker(instrument) that this information is for.")
    news_pieces: list[NewsPiece]


class StockHistoryRequest(BaseModel):
    ticker: str
    period: Literal["1d", "5d", "1mo", "3mo", "6mo"]


# from warrenbotfett.api.yf import InstrumentInformation


#
class PositionAnalysis(BaseModel):
    instrument: str = Field(
        description="Name of the instrument we have an active position in."
    )
    # news_interpretation: InstrumentInformation = Field(description="The full instrument history. This was used (among other things) to make agent desicions.`")
    report: str = Field(
        description="Daily analysis of this position. This should be based on performance as well as recent news and market data."
    )


class BotSummary(BaseModel):
    position_summaries: list[PositionAnalysis] = Field(
        description="Analysis for every position we are active in or consider to be active in."
    )
    overall_summary: str = Field(
        description="An overall summary. This should include other investments that have been considered. Even if they have not been made. We want the reasoning."
    )
    tool_calls: list[ToolCall] = Field(
        description="List of tool calls that the agent has made to make a trade. No tool calls that are just reading data."
    )


class Ticker(BaseModel):
    trading212: str = Field(description="Ticker as used on trading212")


class Trading212Ticker(Enum):
    """Ticker string used for all trading212 endpoints"""

    AAPL_US_EQ = "AAPL_US_EQ"
    MSFT_US_EQ = "MSFT_US_EQ"
    AMZN_US_EQ = "AMZN_US_EQ"
    LLY_US_EQ = "LLY_US_EQ"
    HDId_EQ = "HDId_EQ"
    THREE_V64d_EQ = "3V64d_EQ"
    FB_US_EQ = "FB_US_EQ"
    # # ONE_YDd_EQ = "1YDd_EQ"
    # PG_US_EQ = "PG_US_EQ"
    AMZd_EQ = "AMZd_EQ"
    # XONAd_EQ = "XONAd_EQ"
    # CMCd_EQ = "CMCd_EQ"
    # LLYd_EQ = "LLYd_EQ"
    # WMT_US_EQ = "WMT_US_EQ"
    # ABEAd_EQ = "ABEAd_EQ"
    GOOGL_US_EQ = "GOOGL_US_EQ"
    # MA_US_EQ = "MA_US_EQ"
    # WMTd_EQ = "WMTd_EQ"
    # PRGd_EQ = "PRGd_EQ"
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
    # XOM_US_EQ = "XOM_US_EQ"
    # UNH_US_EQ = "UNH_US_EQ"
    # NVDA_US_EQ = "NVDA_US_EQ"
    # BRYNd_EQ = "BRYNd_EQ"
    # HD_US_EQ = "HD_US_EQ"
    # JNJd_EQ = "JNJd_EQ"
    # BRK_B_US_EQ = "BRK_B_US_EQ"
    # M4Id_EQ = "M4Id_EQ"
    # UNHd_EQ = "UNHd_EQ"
    # FIVE_SPYl_EQ = "5SPYl_EQ"
    # APCd_EQ = "APCd_EQ"
    # JNJ_US_EQ = "JNJ_US_EQ"

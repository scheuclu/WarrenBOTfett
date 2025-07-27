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
    """This datas structure holds a summary of the news articles analyzed for a particular Stock/instrument."""

    name: str = Field("Ticker of the company or instrument that has been analyzed.")
    num_articles: int = Field(
        description="The number of news articles that have been sucessfully processed for this Interpretation.",
        ge=0,
    )
    sentiment: NewsInterpretationSentiment = Field(
        description="A characterization of how the general sentiment of the news articles is. Options are `POSITIVE`, 'NEGATIVE` and `NEUTRAL`. If in doubt, do `NEUTRAL`."
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
    ticker: "YFinanceTicker" = Field(description="The ticker that the news is for.")
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


class YFinanceTicker(Enum):
    AAPL = "AAPL"
    MSFT = "MSFT"
    AMZN = "AMZN"
    LLY = "LLY"
    HDI_DE = "HDI.DE"
    THREE_V64_DE = "3V64.DE"
    META = "META"
    YD1 = "1YD.DE"
    PG = "PG"
    AMZN_ALT = "AMZN"
    XONA = "XONA"
    CMC = "CMC"
    LLY_ALT = "LLY"
    WMT = "WMT"
    ABEA = "ABEA"
    GOOGL = "GOOGL"
    MA = "MA"
    WMT_ALT = "WMT"
    PRG = "PRG"
    V = "V"
    NVDA_ALT = "NVDA"
    AVGO = "AVGO"
    META_ALT = "META"
    CTO = "CTO"
    MSFT_ALT = "MSFT"
    JPM = "JPM"
    TSLA = "TSLA"
    COST = "COST"
    TL0_DE = "TL0.DE"
    XOM = "XOM"
    UNH = "UNH"
    NVDA = "NVDA"
    BRYN = "BRYN"
    HD = "HD"
    JNJ_ALT = "JNJ"
    BRK_B = "BRK-B"
    M4I = "M4I.DE"
    UNH_ALT = "UNH"
    SPY = "SPY"
    APC = "APC"
    JNJ = "JNJ"


class WarrentBOTfettInstrument(BaseModel):
    name: str = Field(description="A human readable name of the company")
    trading212_ticker: Trading212Ticker = Field(
        description="Ticker string used for trading212 APIs"
    )
    yfinance_ticker: YFinanceTicker = Field(
        description="Ticker string used for yfinance APIs"
    )


supported_instruments: list[WarrentBOTfettInstrument] = [
    WarrentBOTfettInstrument(
        name="Apple",
        trading212_ticker=Trading212Ticker.AAPL_US_EQ,
        yfinance_ticker=YFinanceTicker.AAPL,
    ),
    WarrentBOTfettInstrument(
        name="Microsoft",
        trading212_ticker=Trading212Ticker.MSFT_US_EQ,
        yfinance_ticker=YFinanceTicker.MSFT,
    ),
    WarrentBOTfettInstrument(
        name="Amazon",
        trading212_ticker=Trading212Ticker.AMZN_US_EQ,
        yfinance_ticker=YFinanceTicker.AMZN,
    ),
    WarrentBOTfettInstrument(
        name="Eli Lilly",
        trading212_ticker=Trading212Ticker.LLY_US_EQ,
        yfinance_ticker=YFinanceTicker.LLY,
    ),
    WarrentBOTfettInstrument(
        name="Heidelberger Druck",
        trading212_ticker=Trading212Ticker.HDId_EQ,
        yfinance_ticker=YFinanceTicker.HDI_DE,
    ),
    WarrentBOTfettInstrument(
        name="3V64 Fund",
        trading212_ticker=Trading212Ticker.THREE_V64d_EQ,
        yfinance_ticker=YFinanceTicker.THREE_V64_DE,
    ),
    WarrentBOTfettInstrument(
        name="Meta (Facebook)",
        trading212_ticker=Trading212Ticker.FB_US_EQ,
        yfinance_ticker=YFinanceTicker.META,
    ),
    WarrentBOTfettInstrument(
        name="Procter & Gamble",
        trading212_ticker=Trading212Ticker.PG_US_EQ,
        yfinance_ticker=YFinanceTicker.PG,
    ),
    WarrentBOTfettInstrument(
        name="Amazon (alt)",
        trading212_ticker=Trading212Ticker.AMZd_EQ,
        yfinance_ticker=YFinanceTicker.AMZN_ALT,
    ),
    WarrentBOTfettInstrument(
        name="XONA Corp",
        trading212_ticker=Trading212Ticker.XONAd_EQ,
        yfinance_ticker=YFinanceTicker.XONA,
    ),
    # WarrentBOTfettInstrument(
    #     name="CMC",
    #     trading212_ticker=Trading212Ticker.CMCd_EQ,
    #     yfinance_ticker=YFinanceTicker.CMC,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Eli Lilly (alt)",
    #     trading212_ticker=Trading212Ticker.LLYd_EQ,
    #     yfinance_ticker=YFinanceTicker.LLY_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Walmart",
    #     trading212_ticker=Trading212Ticker.WMT_US_EQ,
    #     yfinance_ticker=YFinanceTicker.WMT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="ABEA",
    #     trading212_ticker=Trading212Ticker.ABEAd_EQ,
    #     yfinance_ticker=YFinanceTicker.ABEA,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Google (Alphabet)",
    #     trading212_ticker=Trading212Ticker.GOOGL_US_EQ,
    #     yfinance_ticker=YFinanceTicker.GOOGL,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Mastercard",
    #     trading212_ticker=Trading212Ticker.MA_US_EQ,
    #     yfinance_ticker=YFinanceTicker.MA,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Walmart (alt)",
    #     trading212_ticker=Trading212Ticker.WMTd_EQ,
    #     yfinance_ticker=YFinanceTicker.WMT_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="PROG Holdings",
    #     trading212_ticker=Trading212Ticker.PRGd_EQ,
    #     yfinance_ticker=YFinanceTicker.PRG,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Visa",
    #     trading212_ticker=Trading212Ticker.V_US_EQ,
    #     yfinance_ticker=YFinanceTicker.V,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Nvidia (alt)",
    #     trading212_ticker=Trading212Ticker.NVDd_EQ,
    #     yfinance_ticker=YFinanceTicker.NVDA_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Broadcom",
    #     trading212_ticker=Trading212Ticker.AVGO_US_EQ,
    #     yfinance_ticker=YFinanceTicker.AVGO,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Meta (alt)",
    #     trading212_ticker=Trading212Ticker.FB2Ad_EQ,
    #     yfinance_ticker=YFinanceTicker.META_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="CTO Realty",
    #     trading212_ticker=Trading212Ticker.CTOd_EQ,
    #     yfinance_ticker=YFinanceTicker.CTO,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Microsoft (alt)",
    #     trading212_ticker=Trading212Ticker.MSFd_EQ,
    #     yfinance_ticker=YFinanceTicker.MSFT_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="JPMorgan",
    #     trading212_ticker=Trading212Ticker.JPM_US_EQ,
    #     yfinance_ticker=YFinanceTicker.JPM,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Tesla",
    #     trading212_ticker=Trading212Ticker.TSLA_US_EQ,
    #     yfinance_ticker=YFinanceTicker.TSLA,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Costco",
    #     trading212_ticker=Trading212Ticker.COST_US_EQ,
    #     yfinance_ticker=YFinanceTicker.COST,
    # ),
    # WarrentBOTfettInstrument(
    #     name="TL0 Fund",
    #     trading212_ticker=Trading212Ticker.TL0d_EQ,
    #     yfinance_ticker=YFinanceTicker.TL0_DE,
    # ),
    # WarrentBOTfettInstrument(
    #     name="ExxonMobil",
    #     trading212_ticker=Trading212Ticker.XOM_US_EQ,
    #     yfinance_ticker=YFinanceTicker.XOM,
    # ),
    # WarrentBOTfettInstrument(
    #     name="UnitedHealth",
    #     trading212_ticker=Trading212Ticker.UNH_US_EQ,
    #     yfinance_ticker=YFinanceTicker.UNH,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Nvidia",
    #     trading212_ticker=Trading212Ticker.NVDA_US_EQ,
    #     yfinance_ticker=YFinanceTicker.NVDA,
    # ),
    # WarrentBOTfettInstrument(
    #     name="BRYN",
    #     trading212_ticker=Trading212Ticker.BRYNd_EQ,
    #     yfinance_ticker=YFinanceTicker.BRYN,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Home Depot",
    #     trading212_ticker=Trading212Ticker.HD_US_EQ,
    #     yfinance_ticker=YFinanceTicker.HD,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Johnson & Johnson (alt)",
    #     trading212_ticker=Trading212Ticker.JNJd_EQ,
    #     yfinance_ticker=YFinanceTicker.JNJ_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Berkshire Hathaway B",
    #     trading212_ticker=Trading212Ticker.BRK_B_US_EQ,
    #     yfinance_ticker=YFinanceTicker.BRK_B,
    # ),
    # WarrentBOTfettInstrument(
    #     name="UnitedHealth (alt)",
    #     trading212_ticker=Trading212Ticker.UNHd_EQ,
    #     yfinance_ticker=YFinanceTicker.UNH_ALT,
    # ),
    # WarrentBOTfettInstrument(
    #     name="SP500 ETF",
    #     trading212_ticker=Trading212Ticker.FIVE_SPYl_EQ,
    #     yfinance_ticker=YFinanceTicker.SPY,
    # ),
    # WarrentBOTfettInstrument(
    #     name="APC",
    #     trading212_ticker=Trading212Ticker.APCd_EQ,
    #     yfinance_ticker=YFinanceTicker.APC,
    # ),
    # WarrentBOTfettInstrument(
    #     name="Johnson & Johnson",
    #     trading212_ticker=Trading212Ticker.JNJ_US_EQ,
    #     yfinance_ticker=YFinanceTicker.JNJ,
    # ),
]

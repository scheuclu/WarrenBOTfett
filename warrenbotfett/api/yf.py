from datetime import datetime
from typing import Literal

import yfinance as yf
from pydantic import BaseModel, Field

from warrenbotfett.common import ToolError


class StockHistoryRequest(BaseModel):
    ticker: str = Field("The instrument to get prices for.")
    period: Literal["1d", "5d", "1mo", "3mo", "6mo"] = Field(
        "How many days/months back in time the Stock prices are requested for."
    )


class DailyPrices(BaseModel):
    date: datetime = Field("Day that these prices are for.")
    open: float = Field(description="Opening price on that day")
    high: float = Field(description="Highest Price on that day")
    low: float = Field(description="Lowest price on that day")
    close: float = Field(description="Closing price.")
    volume: int = Field(description="Total number of shared traded that day.")


def get_instrument_history(req: StockHistoryRequest) -> list[DailyPrices] | ToolError:
    """This function can be used to query daily stock prices over a given period up until today."""

    try:
        # Fetch data for Apple Inc. (AAPL)
        tick = yf.Ticker(req.ticker)

        # Get historical data (e.g., last 6 months)
        history = tick.history(period=req.period)  # you c
        return [
            DailyPrices(
                date=date,
                open=row.Open,
                high=row.High,
                low=row.Low,
                close=row.Close,
                volume=row.Volume,
            )
            for date, row in history.iterrows()
        ]
    except Exception as e:
        return ToolError(message=str(e), error_type="RequestError")


if __name__ == "__main__":
    result = get_instrument_history(StockHistoryRequest(ticker="AAPL", period="5d"))
    print(result)

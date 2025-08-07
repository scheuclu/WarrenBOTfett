import asyncio

import httpx
import logfire
import yfinance as yf
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic_ai import Agent, Tool

from warrenbotfett.common import ToolError

load_dotenv()
from dev import extract_article_text
from warrenbotfett.common import (NewsInterpretation, NewsPiece,
                                  RawNewsInformation, YFinanceTicker,
                                  supported_instruments)

logfire.configure()
logfire.instrument_pydantic_ai()


async def read_yahoo_news_article(url: str) -> str:
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

    soup = BeautifulSoup(html, "html.parser")
    body_div = soup.find("div", class_="body")
    if not body_div:
        return ""

    content = await data_collection_agent.run(str(body_div))
    return content.output


async def get_news_articles(ticker: YFinanceTicker) -> RawNewsInformation | ToolError:
    try:
        tick = yf.Ticker(ticker.value)
        news_pieces = []
        for n in tick.news:
            try:
                url = n["content"]["canonicalUrl"]["url"]
                content = await extract_article_text(url)
                news_pieces.append(
                    NewsPiece(
                        title=n["content"]["title"],
                        content=content,
                    )
                )
            except Exception as news_err:
                logfire.warning(f"Skipping news due to: {news_err}")

        return RawNewsInformation(ticker=ticker, news_pieces=news_pieces)
    except Exception as e:
        # raise(e)
        logfire.error(str(e))
        return ToolError(message=str(e), error_type="RequestError")


data_collection_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    system_prompt="Your job is to create a news summary of a given company characterized by a given ticker. "
    "As far as prices go, we look back 1 month by default. You have a tool to get the raw news articles. "
    "THen you just need to extract information and summarize. The output has a field summary. "
    "THis will summarize all the news article that have been analyzed. "
    "You should make at least 500 charcters here if you can. If you dont have any news to process, just write it there.",
    tools=[Tool(function=get_news_articles)],
    end_strategy="exhaustive",
    instrument=True,
    output_type=NewsInterpretation,
)


if __name__ == "__main__":

    async def run_all():
        result = await asyncio.gather(
            *[data_collection_agent.run(supported_instrument.model_dump_json()) for supported_instrument in supported_instruments],
            # data_collection_agent.run('AAPL'),
        )
        return [i.output for i in result]

    import time

    start = time.time()
    result = asyncio.run(run_all())
    for r in result:
        print(r)
    print(time.time() - start)
    print("Done")

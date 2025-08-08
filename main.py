import logfire
from dotenv import load_dotenv
from googlesearch import search
from pydantic_ai import Agent, Tool
from pydantic_ai.agent import AgentRunResult

from warrenbotfett.api.instruments import list_instruments
from warrenbotfett.api.orders import place_buy_order, place_sell_order
from warrenbotfett.api.portfolio import (get_all_positions,
                                         get_specific_position)
# from warrenbotfett.api.yf import get_instrument_history
from warrenbotfett.common import BotSummary
from warrenbotfett.db.write import store_summary
from warrenbotfett.api.yf import read_all_news

search("Google")


logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_requests()

load_dotenv()


from pydantic_ai.models.google import GoogleModelSettings

settings = GoogleModelSettings(google_thinking_config={"include_thoughts": True})

from warrenbotfett.common import supported_instruments, WarrentBOTfettInstrument

def list_supported_instruments() -> list[WarrentBOTfettInstrument]:
    """This function returns the list of all supported investment vehicles. Every vehicle(instrument) has a ticker for Trading212 tools and one for yfinance tools. """
    return supported_instruments

analyst_agent = Agent(
    # model="openai:o3",
    # model="gpt-4o",
    model="google-gla:gemini-2.5-pro",
    # model="google-gla:gemini-2.5-flash",
    model_settings=settings,
    system_prompt=(
        "You are a stock investor that does thorough resaerch before any investments."
        "You have access to trading212 via a bunch of tools."
        "Your first task always is to check the list of instruments(things to invest in) using the tool you got. Call this tool only once. It gives you information for everything."
        "Then you fetch all positions I already have."
        "Next you cehck news and ratings to figure out what is currently good to hold or not."
        "Then you get back to fullfill the user instruction"
    ),
    tools=[
        Tool(function=get_all_positions),
        Tool(function=get_specific_position),
        # Tool(function=list_instruments),
        Tool(function=list_supported_instruments),
        Tool(function=read_all_news),
        Tool(function=place_buy_order),
        Tool(function=place_sell_order),
        # Tool(function=get_instrument_history),
        # tavily_search_tool("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"),
    ],
    end_strategy="exhaustive",  #'early'
    instrument=True,
    output_type=BotSummary,
)


message_history = []
run_result: AgentRunResult[BotSummary] = analyst_agent.run_sync(
    user_prompt="Analyze the market and the current holdings and then make a descion whether to change anyhting."
    "You have all the tools avaialble, so you can trade. Allways read all news, you have a tools for that.  Be desicive. Summarize what you did at the end."
    "You don't have to make a trade if you think that is the best desicion.",
    message_history=message_history,
    parallel=False
)

for message in run_result.all_messages():
    print(message.kind)
    for part in message.parts:
        print(" ", part)


success = store_summary(run_result=run_result)
print(f"{success=}")

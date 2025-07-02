import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, Tool

from warrenbotfett.api.instruments import list_instruments
from warrenbotfett.api.orders import place_buy_order, place_sell_order
from warrenbotfett.api.portfolio import (get_all_positions,
                                         get_specific_position)

# Configure Logfire to capture and send traces
logfire.configure()
logfire.instrument_pydantic_ai()

load_dotenv()


from pydantic import BaseModel, Field


class BotSummary(BaseModel):
    reasoning: str = Field(
        description="a comprehensive reasonsing for the agent desscions. Regardless of whether trades have been made or not."
    )


agent = Agent(
    # model="openai:o3",
    model="gpt-4o",
    # model='google-gla:gemini-2.5-pro',
    deps_type=str,
    system_prompt=(
        "You are a stock investor that does thorough resaerch before any investments."
        "You have access to trading212 via a bunch of tools."
        "Your first task always is to check the list of instruments(things to invest in) using the tool you got."
        "Then you fetch all positions I already have."
        "Next you cehck news and ratings to figure out what is currently good to hold or not"
        "Then you get back to fullfill the user instruction"
    ),
    tools=[
        Tool(function=get_all_positions),
        Tool(function=get_specific_position),
        Tool(function=list_instruments),
        Tool(function=place_buy_order),
        Tool(function=place_sell_order),
    ],
    end_strategy="exhaustive",  #'early'
    instrument=True,
    output_type=BotSummary,
)

result: BotSummary = agent.run_sync(  # type: ignore
    user_prompt="Analyze the market and the current holdings and then make a descion whether to change anyhting. You have all the tools avaialble, so you can trade. Be desicive. Summarize what you did at the end."
)
print(result)

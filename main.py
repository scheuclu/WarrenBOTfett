from dotenv import load_dotenv
from pydantic_ai import Agent

from warrenbotfett.api.instruments import list_instruments
from warrenbotfett.api.orders import place_buy_order, place_sell_order
from warrenbotfett.api.portfolio import (get_all_positions,
                                         get_specific_position)

load_dotenv()

agent = Agent(
    "openai:o3",
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
        get_all_positions,
        get_specific_position,
        list_instruments,
        place_buy_order,
        place_sell_order,
    ],
    end_strategy="exhaustive",  #'early'
    instrument=True,
)


dice_result = agent.run_sync(  # type: ignore
    user_prompt="Analyze the market and the current holdings and then make a descion whether to change anyhting. You have all the tools avaialble, so you can trade. Be desicive. Summarize what you did at the end."
)

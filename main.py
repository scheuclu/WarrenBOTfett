import sys

import logfire
from dotenv import load_dotenv
from googlesearch import search
from pydantic_ai import Agent, Tool
from pydantic_ai.agent import AgentRunResult

from warrenbotfett.api.orders import place_buy_order, place_sell_order
from warrenbotfett.api.portfolio import (get_all_positions,
                                         get_specific_position)
from warrenbotfett.api.yf import read_all_news
from warrenbotfett.common import BotSummary2
from warrenbotfett.db.write import store_summary

search("Google")


logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_requests()

load_dotenv()


from pydantic_ai.models.google import GoogleModelSettings

from warrenbotfett.common import (BuyOrder, WarrentBOTfettInstrument,
                                  supported_instruments)


def in_streamlit():
    return "streamlit" in sys.modules


def list_supported_instruments() -> list[WarrentBOTfettInstrument]:
    """This function returns the list of all supported investment vehicles. Every vehicle(instrument) has a ticker for Trading212 tools and one for yfinance tools."""
    return supported_instruments


from pydantic_ai.models import KnownModelName


def run_agent(
    model: KnownModelName = "google-gla:gemini-2.5-pro",
) -> AgentRunResult[BotSummary2]:
    settings = GoogleModelSettings(google_thinking_config={"include_thoughts": True})
    analyst_agent = Agent(
        model=model,
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
            Tool(function=list_supported_instruments),
            Tool(function=read_all_news),
            Tool(function=place_buy_order),
            Tool(function=place_sell_order),
        ],
        end_strategy="exhaustive",  #'early'
        instrument=True,
        output_type=BotSummary2,
    )

    message_history = []
    run_result: AgentRunResult[BotSummary2] = analyst_agent.run_sync(
        user_prompt="Analyze the market and the current holdings and then make a descion whether to change anyhting. You have all the tools avaialble, so you can trade. Allways read all news, you have a tools for that.  Be desicive. Summarize what you did at the end. You don't have to make a trade if you think that is the best desicion.",
        message_history=message_history,
    )
    return run_result


if __name__ == "__main__":
    run_result: AgentRunResult[BotSummary2]

    if in_streamlit():
        import streamlit as st

        FAST_MODEL: KnownModelName = "google-gla:gemini-2.5-pro"
        PRO_MODEL: KnownModelName = "google-gla:gemini-2.5-flash"

        @st.cache_data(ttl=3600)
        def run_cached_agent(model: KnownModelName = "google-gla:gemini-2.5-pro"):
            return run_agent(model=model)

        st.header("Streamlit detected")
        with st.spinner():
            run_result: AgentRunResult[BotSummary2] = run_cached_agent(model=PRO_MODEL)
        st.text(run_result.output.overall_summary)
        st.subheader("Holdings analysis")
        for position_analysis in run_result.output.position_summaries:
            with st.expander(label=position_analysis.instrument):
                st.text(position_analysis.report)
        st.subheader("Actions")
        for action in run_result.output.actions:
            # st.text(type(action))
            if isinstance(action, BuyOrder):
                st.markdown(f"**BUY** {action.amount} of {action.instrument.name}")
                st.text(action.reasoning)
            else:
                st.markdown(f"**SELL** {action.instrument.name}")
                st.text(action.reasoning)
    else:
        run_result: AgentRunResult[BotSummary2] = run_agent()

        for message in run_result.all_messages():
            print(message.kind)
            for part in message.parts:
                print(" ", part)
        success = store_summary(run_result=run_result)
        print(f"{success=}")

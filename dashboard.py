import datetime

import plotly.graph_objects as go
import streamlit as st

from warrenbotfett.common import BotSummary, ToolCall
from warrenbotfett.db.read import read_sp500_benchmark, read_summary

st.set_page_config(layout="wide")

# "with" notation
with st.sidebar:
    st.title("WarrenBOTfett")
    st.markdown("---")
    st.image("./WarrenBOTfet_nobg.png", width=120)
    st.markdown("---")
    st.text(
        "WarrentBOTfett is a fully automated AI investor actively trading SP500 stocks. It is connected to an active broker."
    )
    st.markdown("---")
    st.markdown("[Performance vs SP500](#warren-bo-tfett)")
    st.markdown("[Desicion History](#agent-desicion-history)")


# st.title("WarrenBOTfett")
# st.text("Tracking the desicions the agent makes over time.")

# st.markdown("---")

# st.divider()
summaries: dict[datetime.datetime, BotSummary] = read_summary()
sp500_benchmark = read_sp500_benchmark()

trace_sp500 = go.Scatter(
    x=[row["created_at"] for row in sp500_benchmark],
    y=[
        row["sp500_price"] / sp500_benchmark[-1]["sp500_price"]
        for row in sp500_benchmark
    ],
    name="SP500 benchmark",
)
trace_portfolio = go.Scatter(
    x=[row["created_at"] for row in sp500_benchmark],
    y=[
        row["portfolio_value"] / sp500_benchmark[-1]["portfolio_value"]
        for row in sp500_benchmark
    ],
    name="WarrenBOTfett portfolio",
)
layout = go.Layout(title="WarrenBOTfett vs. SP500")
fig = go.Figure(data=[trace_sp500, trace_portfolio])
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)
st.subheader("Performance vs SP500")
st.plotly_chart(fig, config={"displayModeBar": False})


cols = st.columns([2, 10])

st.markdown("---")
st.subheader("Agent desicion history")
st.text(
    "Below is a detailed history of all desicions the agent has made. Day by day. Note that the is is an ongoing projects, so most recent runs are probably mroe sophisticated than older ones."
)
for i, (date, s) in enumerate(reversed(summaries.items())):
    with st.expander(
        label=f"Investment desicion Summary - {date.strftime('%Y-%m-%d')}",
        expanded=i == 0,
    ):
        # st.markdown("# Reasoning")

        cols = st.columns([1, 11])
        with cols[0]:
            st.image("./WarrenBOTfet_nobg.png")
        with cols[1]:
            st.markdown("## Holdings")
            for summary in s.position_summaries:
                st.markdown(f" - {summary.instrument}")
                st.markdown(summary.report)
        st.markdown("## Summary")
        st.markdown(s.overall_summary)

        st.markdown("## Actions")

        tool_calls: list[ToolCall] = s.tool_calls

        reasoning_string = "\n".join(
            [" - " + tool_call.reasoning for tool_call in tool_calls]
        )
        st.markdown(reasoning_string)

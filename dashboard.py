import datetime

import streamlit as st
import plotly.graph_objects as go
from warrenbotfett.common import BotSummary, ToolCall
from warrenbotfett.db.read import read_summary, read_sp500_benchmark

st.set_page_config(layout="wide")

st.title("WarrenBOTfett")
st.text("Tracking the desicions the agent makes over time.")
# st.divider()
summaries: dict[datetime.datetime, BotSummary] = read_summary()
sp500_benchmark = read_sp500_benchmark()

trace_sp500=go.Scatter(
    x=[row['created_at'] for row in sp500_benchmark],
    y=[row['sp500_price']/sp500_benchmark[-1]['sp500_price'] for row in sp500_benchmark],
    name='SP500 benchmark'
)
trace_portfolio=go.Scatter(
    x=[row['created_at'] for row in sp500_benchmark],
    y=[row['portfolio_value']/sp500_benchmark[-1]['portfolio_value'] for row in sp500_benchmark],
    name='WarrenBOTfett portfolio'
)
layout=go.Layout(title="WarrenBOTfett vs. SP500")
fig=go.Figure(data=[trace_sp500, trace_portfolio], layout=layout)
st.plotly_chart(fig)


cols = st.columns([2, 10])


st.subheader("History")
for i, (date, s) in enumerate(reversed(summaries.items())):
    with st.expander(label=date.strftime("%Y-%m-%d"), expanded=i==0):
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

import datetime

import streamlit as st

from warrenbotfett.common import BotSummary, ToolCall
from warrenbotfett.db.read import read_summary

st.set_page_config(layout="wide")

st.title("WarrenBOTfett")
st.text("Tracking the desicions the agent makes over time.")
# st.divider()
summaries: dict[datetime.datetime, BotSummary] = read_summary()


cols = st.columns([2, 10])


st.subheader("History")
for date, s in summaries.items():
    with st.expander(label=date.strftime("%Y-%m-%d"), expanded=True):
        st.markdown("### Reasoning")

        cols = st.columns([1, 11])
        with cols[0]:
            st.image("./WarrenBOTfet_nobg.png")
        with cols[1]:
            st.markdown(s.reasoning)

        st.markdown("### Actions")

        tool_calls: list[ToolCall] = s.tool_calls

        reasoning_string = "\n".join(
            [" - " + tool_call.reasoning for tool_call in tool_calls]
        )
        for i, too_call in enumerate(tool_calls):
            st.markdown(reasoning_string)

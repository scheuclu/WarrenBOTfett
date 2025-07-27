import streamlit as st

st.set_page_config(layout="wide")

st.title("WarrenBOTfett")
st.subheader("Stock news")
st.text("Below are my opinions on the currently supported stocks based on recent news.")

import asyncio

import streamlit as st

from warrenbotfett.api.yf import data_collection_agent
from warrenbotfett.common import (NewsInterpretation,
                                  NewsInterpretationSentiment,
                                  supported_instruments)


async def run_all() -> list[NewsInterpretation]:
    result = await asyncio.gather(
        *[
            data_collection_agent.run(instrument.model_dump_json())
            for instrument in supported_instruments
        ]
    )
    return [r.output for r in result]


@st.cache_data(ttl=86000)
def get_results() -> list[NewsInterpretation]:
    result: list[NewsInterpretation] = asyncio.run(run_all())
    return result


for info in get_results():
    st.subheader(info.name)
    st.markdown(f"**number or articles:** {info.num_articles}")
    content = info.summary.replace("$", r"\$")
    # st.markdown(f"### {news.title}")
    if info.sentiment == NewsInterpretationSentiment.POSITIVE:
        st.success(content)
    elif info.sentiment == NewsInterpretationSentiment.NEGATIVE:
        st.error(content)
    else:
        st.warning(content)

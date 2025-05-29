import openai
import streamlit as st
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
os.getenv("OPENAI_API_KEY")

try:
    from agents import Agent, Runner, WebSearchTool, trace
except ImportError:
    st.error("The required 'agents' module or related tools are missing.Ensure all dependencies are installed.")
    st.stop()

async def get_web_search_update(city,topic):
    """
        Async function to run the agent and fetch web search result for the given city and topic.
    """
    agent = Agent(
        name="Web Searcher",
        instructions="You are a helpful agent.",
        tools=[WebSearchTool(user_location={"type": "approximate", "city": "city"})],
    )
    with trace("Web search example"):
        result = await Runner.run (
            agent,
            f"search the web for '{topic} news in {city} and give me 3 interesting update in a sentence.",
        )
    return result.final_output

st.title("Web Search: Open AI Agent Interface")
st.write("This application uses an  OpenAI Agent to fetch **specific updates** by city and topic.")

with st.form("city_topic_form"):
    st.text ("Please enter only a city name and topic word to fetch the update using web search.")
    user_city = st.text_input("Enter a city:",placeholder="e.g., New York, London, Tokyo")
    user_topic = st.text_input("Enter a news topic:",placeholder="e.g., sports,technology,weather,travel")
    submitted= st.form_submit_button("Submit")

if submitted:
    if user_city.strip() == "" or user_topic.strip() == "":
        st.error("Please enter both valid city name and topic.")
    else:
        st.info(f"Fetching **{user_topic}** from **{user_city}**...Please wait.")

        try:
            result = asyncio.run(get_web_search_update(user_city, user_topic))
            st.success(f"Here's the interesting {user_topic} update for {user_city}:")
            st.markdown(f"**{result}**")
        except Exception as e:
            st.error(f"AN error occurred while fetching the update: {e}")

st.write("---")
st.caption("Powered by OpenAI Agent")

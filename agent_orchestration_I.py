
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
os.getenv("OPENAI_API_KEY")

import asyncio
from agents import Agent, ItemHelpers, MessageOutputItem,Runner, trace

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate user's message to Spanish",
    handoff_description="An english to spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate user's message to French",
    handoff_description="An english to french translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate user's message to Italian",
    handoff_description="An english to italian translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations,you call for relevent tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="tanslate_to_spanish",
            tool_description="Translate user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="tanslate_to_french",
            tool_description="Translate user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="tanslate_to_italian",
            tool_description="Translate user's message to Italian",
        ),
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations,crrect them if needed , and produce a final concatenated response.",
)

async def main():
    msg = input("Hi! What would you like to translate and to which languages?")

    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f" - Translation step: {text}")
        synthesizer_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list()

        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

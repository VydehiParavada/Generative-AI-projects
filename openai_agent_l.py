import os
from dotenv import load_dotenv

load_dotenv()

os.getenv("OPENAI_API_KEY")

from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, input="How does brain react when something happens physically?")

print(result.final_output.strip())

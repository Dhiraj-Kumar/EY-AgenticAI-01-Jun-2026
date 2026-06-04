from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

agent = AssistantAgent("assistant", llm)

async def main():
    while True:
        user_input = input("You: ")
        if user_input=="exit":
            break
        result = await agent.run(task=user_input)
        print(f"AI: {result.messages[-1].content}")

asyncio.run(main())
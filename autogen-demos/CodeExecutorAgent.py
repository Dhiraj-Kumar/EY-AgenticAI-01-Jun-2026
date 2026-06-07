from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

work_directory = os.path.abspath("demo_files")

executor = LocalCommandLineCodeExecutor(work_dir=work_directory)
executor_agent = CodeExecutorAgent(
    name="executor",
    code_executor=executor
)

coder = AssistantAgent(
    name = "coder",
    model_client=llm,
    system_message=f"""
    You are an expert python programmer.
    Your workspace is {work_directory}.
    1. Always write code in python markdown blocks.
    2. When creating data, explictly save it to a file (CSV, TXT, JSON etc.)
    3. If the executor returns an error, fix it.
    """
)

team = RoundRobinGroupChat(
    participants=[coder, executor_agent],
    max_turns=2
)


async def main():
    await Console(team.run_stream(task="Create a CSV file name users.csv with 5 rows of dummy user data (name, email)"))
    
asyncio.run(main())
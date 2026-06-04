from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

# Agent 1. Writer Agent
writer = AssistantAgent (
    name="writer",
    model_client=llm,
    system_message="""
    You are a creative writer. Write a 3-part thread about the user's topic.
    End your message with the exact tag: [WRITING_DONE]
    """   
)

# Agent 2. Auditor Agent
auditor = AssistantAgent(
    name="auditor",
    model_client=llm,
    system_message="""
    You are a fact checker. Review the writer's work for accuracy.
    If the content has issues, end with [AUDIT_FAILED].
    iF THE content is acceptable, end with [AUDIT_PASSED].
    Always end with exactly on of these tags.
    """
)

# Agent 3. Publisher Agent
publisher = AssistantAgent(
    name="publisher",
    model_client=llm,
    system_message="""
    You are a professional publisher with expertise in formatting. Add emojis and clean formatting. End your message with: [PUBLISHED] and the word 'FINISH'
    """
)

def selector_fn(message):
    last_message = message[-1]
    content = last_message.content if hasattr(last_message, "content") else ""
    
    if last_message.source == "user":
        return "writer"
    if "[WRITING_DONE]" in content:
        return "auditor"
    if "[AUDIT_PASSED]" in content:
        return "publisher"
    if "[AUDIT_FAILED]" in content:
        return "writer"

team = SelectorGroupChat(
    participants=[writer, auditor, publisher],
    model_client=llm,
    termination_condition=TextMentionTermination("FINISH"),
    selector_prompt="""
    You are a selection manager. Choose the next agent based on only the most recent message.
    
    Routing roules (strict order):
    1. If the message is from the user -> writer
    2. If the message contains [WRITING_DONE] -> auditor
    3. If the message contains [AUDIT_PASSED] -> publisher
    4. If the message contains [AUDIT_FAILED] -> writer
    
    ouput rules:
    - Output ONLY on of: writer, auditor, publisher
    - No explanations
    - No extra text
    """,
    selector_func=selector_fn
)

async def main():
    await Console(team.run_stream(task="The future of Mars Colonization"))

asyncio.run(main())
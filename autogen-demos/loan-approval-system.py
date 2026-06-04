from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

agent = AssistantAgent("assistant", llm)

# Agent 1. Credit Analyst Agent
credit_analyst = AssistantAgent(
    name="credit_analyst",
    model_client=llm,
    system_message="""
    You are a Senior Credit Analyst. Your goal is to assess creditworthness beyond the raw score.
    Constraints:
    - If credit Score < 600: Immediate rejection recommended.
    -If Score > 600: Analyze 'debit-to-credit' utilization. Mention if high utilization is a risk.
    - Requirements: You must explicitly state 'CREDIT_VERIFIED' to proceed.
    - Output: Summarize key credit risks or confirm stability in 2 sentences.
    """
)

# Agent 2. Risk Assessor Agent
risk_assessor = AssistantAgent(
    name="risk_assessor",
    model_client=llm,
    system_message="""
    You are a risk underwriter. You evaluate the 'Debt-To-Income' (DTI) ratio.
    Constraints:
    - Formula: Monthly Loan Payment / (Annual Income /12)
    - If DTI > 30%: Flag as 'High Risk'
    - If Loan Amount > '50%' of Annual Income: Flag as 'Over-leveraged'.
    - Requirements: You must acknowledge the credit analyst's notes.
    - Output: State 'RISK_ASSESSED' and proved a risk tier: Low, Medium or High.
    """
)

# Agent 3. Final Approver Agent
final_approver = AssistantAgent(
    name="final_approver",
    model_client=llm,
    system_message="""
    You are the Loan Officer with final signatory authority.
    Constraints:
    - Decision Logic: You can only approve if you see Both 'CREDIT_VERIFIED' and 'RISK_ASSESSED'
    - Compliance: if either agent flagged a 'High Risk', you must provied a counter measure (e.g., higher interest rate) or reject.
    - Output: Your response must be a formal memo.
    - Termination: End with 'VERDICT: [APPROVED/REJECTED]' followed by 'FINISH'
    """
)

team = RoundRobinGroupChat(
    participants=[credit_analyst, risk_assessor, final_approver],
    termination_condition=TextMentionTermination("FINISH")
)

async def main():
    await Console(team.run_stream(task="Applicant: Peter Parker. Credit Score: 720. Annual Income: $20,000. Loan Requested: $5000"))

asyncio.run(main())
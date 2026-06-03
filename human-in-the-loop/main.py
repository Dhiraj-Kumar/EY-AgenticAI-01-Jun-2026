from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command
import resend
from typing import Literal

load_dotenv()

class Feedback(BaseModel):
    participant_name: str = Field(description="Name of the participant. Keep it blank if no name is provided in the feedback")
    summary: str = Field(description="Brief summary if the overall feedback")
    sentiment: Literal['positive', 'negative'] = Field(description="Sentiment of the feedback like positive or negative")
    highlights: list[str] = Field(description="List of positive higlights of the program described by the participants")
    lowlights: list[str] = Field(description="List of negative higlights of the program described by the participants")
    rating: str = Field(description="Rating for the program. Mark as 'None' if rating is not provided")
    email_address: str = Field(description="Email address of the participant")

llm = ChatOpenAI(model="gpt-4.1-2025-04-14")

@tool
def send_email(email_address, body):
    """
    Tool for sending email
    """
    resend.api_key="re_TFsAuxzv_4epUYk1ukxLyct781DaNTGLC"
    params: resend.Emails.SendParams = {
        "from": "training@resend.dev",
        "to": [email_address],
        "subject": "Reply from Training Manager",
        "html": body
    }
    print(body)
    email = resend.Emails.send(params)
    return email


agent = create_agent(
    model=llm,
    response_format=Feedback,
    checkpointer=InMemorySaver(),
    system_prompt="You are an AI assistant who analye the customer feedback and send an email to customer based on feedback sentiment. If sentiment is positive, you send a thank you email and if sentiment is negative you send an apology email. You use tools to send email. Use html format to draft an email.",
    tools=[send_email],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions":["approve", "reject"]
                }
            }
        )
    ]
)

response = agent.invoke({
    "messages": [{"role": "user", "content": "The Java Fullstack training program was well-structured and covered essential modules like Core Java, Spring Boot, Hibernate, and Angular. The hands-on projects and live coding sessions made it easier to apply concepts in real-world scenarios. The trainer was knowledgeable and supportive, and the sessions on Git and deployment provided a complete view of end-to-end development. However, the pace during the Spring Boot section felt a bit fast, and more time for practice would have been helpful. Additionally, a dedicated session on debugging and code optimization could enhance the learning experience. Some front-end sessions, especially on Angular, felt rushed, and could benefit from more real-time examples. Out of 5 I would give 4 rating for this program. Feedback given by Dhiraj Kumar. Email address - dhiraj2001@gmail.com."}]
}, {"configurable": {"thread_id": "1"}})

if "__interrupt__" in response:
    print("Workflow paused... waiting for human approval")
    print("1. Approve\n2. Reject")
    user_input = input("Enter your choice: ")
    choices = {"1": "approve", "2": "reject"}
    result = agent.invoke(
        Command(
            resume={
                "decisions": [
                    {
                        "type": choices.get(user_input)
                    }
                ]
            }
        ), {"configurable": {"thread_id": "1"}}
    )

    print(f"Result: {result['messages'][-1].content}")
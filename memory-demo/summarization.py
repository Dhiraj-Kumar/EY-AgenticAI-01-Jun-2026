from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
summarization_llm = ChatOpenAI(model="gpt-3.5-turbo")

agent = create_agent(
    model=llm,
    system_prompt="You are an AI assistant who answer user queries politely.",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model=summarization_llm,
            # trigger=("tokens", 4000)
            trigger=("fraction", 0.2),
            keep=("messages", 4)
        )
    ]
)

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break;
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    }, {"configurable": {"thread_id": "1"}})
    
    print(f"AI: {response['messages'][-1].content}")
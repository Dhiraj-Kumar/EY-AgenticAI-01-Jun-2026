from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    system_prompt="You are an AI assistant who answer user queries politely.",
    checkpointer=InMemorySaver()
)

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break;
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    }, {"configurable": {"thread_id": "1"}})
    
    print(f"AI: {response['messages'][-1].content}")
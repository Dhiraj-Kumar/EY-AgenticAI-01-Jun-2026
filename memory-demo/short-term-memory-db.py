from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

DB_URI = "postgresql://postgres:niit1234@localhost:5432/conversationdb?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent(
        model=llm,
        system_prompt="You are an AI assistant who answer user queries politely.",
        checkpointer=checkpointer
    )

    while True:
        user_input = input("You: ")
        if user_input.lower()=="exit":
            break;
        response = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        }, {"configurable": {"thread_id": "1"}})
        
        print(f"AI: {response['messages'][-1].content}")
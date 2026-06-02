from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4.1-2025-04-14")

chat_history=[
    SystemMessage(content="""
        You are a helpful AI assistant who answers query with a bit of humour.
        Make the responses funny without losing the context of the question.
        Include the mojis for making your responses looks attractive.
    """)
]

for chunk in model.stream("Explain polymorphism. Give code examples"):
    print(chunk.content, end="", flush=True)

# while True:
#     user_input = input("You: ")
#     if(user_input=="exit"):
#         break
#     chat_history.append(HumanMessage(content=user_input))
#     result = model.invoke(chat_history)
#     chat_history.append(AIMessage(content=result.content))
#     print(f"AI: {result.content}")

# print(chat_history)
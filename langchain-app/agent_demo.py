from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

OPENWEATHERMAP_API_KEY=os.getenv("OPENWEATHERMAP_API_KEY")

@tool
def getWeatherInfo(city: str):
    """
    Get the current weather of a city using openweathermap api
    """
    url="https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params)
    if response.status_code != 200:
        return "Unable to fetch the data from api"
    
    return response.json()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    system_prompt="You are an AI weather assistant who only responds to the qquery asked about weather information. You call tools to access latest weather information. DO NOT respond to any other questions which is not about weather forecast. Maintain a friendly tone with a bit of humour. Add emojis to make your responses looks good.",
    tools=[getWeatherInfo]
)

while True:
    user_input = input("You: ")
    if user_input=="exit":
        break
    result = agent.invoke({"messages":[
        {"role": "user", "content": user_input}
    ]})
    # print(f"AI: {result["messages"][-1].content}")
    print(result["messages"][-1].content)

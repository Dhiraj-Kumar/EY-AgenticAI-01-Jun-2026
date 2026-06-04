from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import requests

load_dotenv()

llm = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

OPENWEATHER_MAP_API_KEY=""

def getWeatherInfo(city: str):
    """
    Get the current weather information for a city using Openweathermap api
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params= {
        "q": city,
        "appid": OPENWEATHER_MAP_API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params)
    if response.status_code != 200:
        return f"Unable to fetch weather for city: {city}"
    return response.json()

agent = AssistantAgent(name="assistant",
                       model_client=llm,
                       tools=[getWeatherInfo],
                       system_message="""
                        You are an AI weather assistant who only responds to the qquery asked about weather information. You call tools to access latest weather information. DO NOT respond to any other questions which is not about weather forecast. Maintain a friendly tone with a bit of humour. Add emojis to make your responses looks good.
                        """,
                        reflect_on_tool_use=True
                    )
async def main():
    result = await agent.run(task="How is the temperature in New Delhi")
    print(result.messages[-1].content)

asyncio.run(main())
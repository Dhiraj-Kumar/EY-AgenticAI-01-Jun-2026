from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini"
)

tavily_tool = TavilySearch(max_results=3)

research_agent = create_agent(
    model = llm,
    system_prompt="""
    You are a research agent whose task is to gather accurate and up-to-date information from the internet using available search or browsing tool. when a query is given, use the tools to find reliable sources, extract relevant facts, and summarize the information clearly and concisely. If multiple sources are found, consolidate key points and note any uncertainities or limitations before returning results
    """,
    checkpointer=InMemorySaver(),
    tools=[tavily_tool]
)

writer_agent = create_agent(
    model=llm,
    system_prompt="""
    You are a writer agent responsible for converting inputs from other agents into clear, well-organized and readable content. Use the provided information as-is without adding new facts or performing research. Present the output in a logical flow with concise language, proper headings or bullet points whichever appropriate, and a professional tone. Your goal is to clearly communicate the information to the intended audience while maintaining accuracy and clarity.
    """
)


@tool
def research_agent_tool(query: str):
    """
    Gather accurate and up-to-date information from the internet based on user query and performs deep research.
    """
    result = research_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    return result['messages'][-1].content

@tool
def writer_agent_tool(research_text: str):
    """
    Writes the content in well organized, and readable format based in research text. Use table or bulleted list wherever required. Your final response must be in markdown format.
    """
    result = writer_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": research_text
            }
        ]
    })
    return result['messages'][-1].content

main_agent = create_agent(
    model=llm,
    system_prompt="You are an AI assistant who takes input from user and delegate task to sub agents. You use tools to invoke sub agents.",
    tools=[research_agent_tool, writer_agent_tool],
    checkpointer=InMemorySaver()
)

result = main_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Do a thorough research on the GDP of India based on latest 2025 reports and write a complete article."
        }
    ]
}, config={"configurable": {"thread_id": 1}})

print(result['messages'][-1].content)
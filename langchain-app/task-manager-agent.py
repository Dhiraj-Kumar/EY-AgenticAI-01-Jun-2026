from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import sqlite3

load_dotenv()

con = sqlite3.connect("taskdb.db", check_same_thread=False)
cursor = con.cursor()

# Create table if it does not exists
cursor.execute("""
    Create table if not exists todos (
        id integer primary key autoincrement,
        todo text not null,
        iscompleted boolean not null
    )
""")

con.commit()

@tool
def add_todo(todo: str):
    """
    Add a new todo in todos table in database
    """
    cursor.execute("insert into todos (todo, iscompleted) values (?, ?)", (todo, False))
    con.commit()

@tool
def get_all_todos():
    """
    Get all todos from todos table
    """
    cursor.execute("Select id, todo, iscompleted from todos Order By id")
    return cursor.fetchall()

@tool
def get_todo_by_id(todo_id: str):
    """
    Get todo item from todos table based on todo_id
    """
    cursor.execute("Select id, todo, iscompleted from todos where id=?", (todo_id,))
    return cursor.fetchone()

@tool
def delete_todo(todo_id):
    """
    Delete a todo item from todos table based on todo_id
    """
    cursor.execute("Delete from todos where id=?",(todo_id,))
    con.commit()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    system_prompt="You are an AI todo assistant who who helps in managing tasks for the user. you call tools to perform different actions. You are strictly managing the todos and do not answer queries related to anything else",
    tools=[add_todo, get_all_todos, get_todo_by_id, delete_todo]
)

while True:
    user_input = input("You: ")
    if user_input=="exit":
        break
    result = agent.invoke({"messages":[
        {"role": "user", "content": user_input}
    ]})
    print(result["messages"][-1].content)

print(result)
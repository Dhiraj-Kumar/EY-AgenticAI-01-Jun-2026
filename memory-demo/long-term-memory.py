from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langgraph.store.memory import InMemoryStore

load_dotenv()

embed_model = OpenAIEmbeddings(model="text-embedding-3-small")


store = InMemoryStore(index={"embed": embed_model, "dims": 768})
namespace = ("user1", "chitchat")

# Storing the data in long term memory store
store.put(
    namespace,
    "user_info",
    {"user_name": "Dhiraj", "Tone": "formal"}
)

# Again storing more data in long term memory store
store.put(namespace, "personalization", {"theme": "dark"})

# Searching the info by passing natural human text
search_result = store.search(namespace, query="What is the name of the user?", limit=1)

for item in search_result:
    print(item.value)
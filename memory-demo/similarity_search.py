from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

docs = [
    "The Eiffel Tower in Paris is a wrought-iron structure known for its iconic design and panoramic city views.",
    "The Great Wall of China is an ancient series of fortifications built to protect against invasions and spans thousands of miles.",
    "The Statue of Liberty in New York symbolizes freedom and democracy, and was a gift from France to the United States."
]

query = "Which structure is made of Iron"

doc_embeddings = [get_embedding(doc) for doc in docs]
query_embedding = get_embedding(query)

score = cosine_similarity([query_embedding], doc_embeddings)[0]

print(score)

best_index, best_score = max(enumerate(score), key=lambda x: x[1])

print("Most similar document: ")
print(docs[best_index])
print(f"Similarity Score is: {best_score}")
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# model = ChatOpenAI(model="gpt-4o-mini")

# template = PromptTemplate(template="Write an article on {topic}", input_variables=["topic"], validate_template=True)

# prompt = template.invoke({'topic': 'AI'})

# result = model.invoke(prompt)

# template2 = PromptTemplate(template="Generate 5 multiple choice questions with answers based on the following article:\n{text}", input_variables=["text"])

# prompt2 = template2.invoke({'text': result.content})

# result2 = model.invoke(prompt2)

# print(result.content)
# print(result2.content)

model = ChatOpenAI(model="gpt-4o-mini")

template1 = PromptTemplate(template="Write an article on {topic}", input_variables=["topic"], validate_template=True)

template2 = PromptTemplate(template="Generate 5 multiple choice questions with answers based on the following article:\n{text}. Complexity level is {level}", input_variables=["text", "level"])

chain = template1 | model | StrOutputParser() | (lambda article: {"text": article, "level": RunnablePassthrough()}) | template2 | model | StrOutputParser() #LCEL

print(chain.invoke({'topic': 'Cyber Security', 'level': 'Intermediate'}))


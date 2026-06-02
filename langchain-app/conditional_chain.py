from typing import Literal
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description="Give the sentiment of the feedbck")

pyparser = PydanticOutputParser(pydantic_object=Feedback)

template = PromptTemplate(template="Analyze the sentiment of the following feedback and classify it into positive or negative \n {feedback} \n {format_instructions}", input_variables=["feedback"], partial_variables={'format_instructions': pyparser.get_format_instructions()})

chain1 = template | model | pyparser

positive_email_template = PromptTemplate(template="Write a thank you mail to the cutomer for giving a positive feedback about his recent purchase of IPhone 17. \n {feedback}", input_variables=["feedback"])

negative_email_template = PromptTemplate(template="Write an apology mail to the cutomer for giving a negative feedback about his recent purchase of IPhone 17. \n {feedback}", input_variables=["feedback"])

# Writing the conditional branch
branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', positive_email_template | model | StrOutputParser()),
    (lambda x:x.sentiment == 'negative', negative_email_template | model | StrOutputParser()),
    (lambda x:"Not able to analyze the sentiment")
)

final_chain = chain1 | branch_chain

# print(final_chain.invoke({'feedback': 'The phone is very good and meeting all my expectations'}))
print(final_chain.invoke({'feedback': 'The phone is really not meeting my expectations. I am disappointed'}))
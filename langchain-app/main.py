from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Feedback(BaseModel):
    participant_name: str = Field(description="Name of the participant. Keep it blank if no name is provided in the feedback")
    summary: str = Field(description="Brief summary if the overall feedback")
    sentiment: str = Field(description="Sentiment of the feedback like positive, negative or neutral")
    highlights: list[str] = Field(description="List of positive higlights of the program described by the participants")
    lowlights: list[str] = Field(description="List of negative higlights of the program described by the participants")
    rating: str = Field(description="Rating for the program. Mark as 'None' if rating is not provided")

model = ChatOpenAI(model="gpt-4o-mini")

structured_model = model.with_structured_output(Feedback)

# result = structured_model.invoke("The Java Fullstack training program was well-structured and covered essential modules like Core Java, Spring Boot, Hibernate, and Angular. The hands-on projects and live coding sessions made it easier to apply concepts in real-world scenarios. The trainer was knowledgeable and supportive, and the sessions on Git and deployment provided a complete view of end-to-end development. However, the pace during the Spring Boot section felt a bit fast, and more time for practice would have been helpful. Additionally, a dedicated session on debugging and code optimization could enhance the learning experience. Some front-end sessions, especially on Angular, felt rushed, and could benefit from more real-time examples. Out of 5 I would give 4 rating for this program. Feedback given by Dhiraj Kumar")

result = structured_model.invoke("Training was not as per the expectation")

print(result.summary)
print(result.sentiment)

print(result)
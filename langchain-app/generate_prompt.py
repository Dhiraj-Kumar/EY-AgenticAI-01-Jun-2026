from langchain_core.prompts import PromptTemplate

template = PromptTemplate(template="""
You are a professional travel planner. Based on the user's profile, create a personalized travel itinerary. Include activities, must-see attractions, suggested local food, transportation tips, cultural do's and dont's and a basic packing checklist.
User Info:
- Name: {username}
- Destination: {destination}
- Travel Date: {start_date} to {end_date}
- Budget: {budget}
- Interest: {interests}
- Travel Style: {travel_style}
- Dietary Preferences: {dietary_preferences}

Ensure the plan fits the user's budget and travel style. Highlight one unique or offbeat experience they shouldn't miss. Keep the tone friendly and informative.
""", input_variables=['username', 'desitnation', 'start_date', 'end_date', 'budget', 'interests', 'travel_style', 'dietary_preferences'])

template.save('travel_planner_template.json')
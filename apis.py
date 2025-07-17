import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
load_dotenv()


genai.configure(api_key=os.environ.get("GENAI_KEY"))



def genai_fitness_plan(height, weight, goal, age=None, gender=None):
    # Build a natural language description from user inputs
    try:
        user_desc = f"someone who is {height} tall, weighs {weight} lbs"
        if age:
            user_desc += f", {age} years old"
        if gender:
            user_desc += f", {gender}"

        # Final prompt
        prompt = (
            "You are a certified fitness coach who creates motivating, beginner-friendly workout plans "
            "based on people's body stats and fitness goals. Avoid jargon.\n\n"
            f"Create a simple 1-week beginner workout plan for {user_desc}. "
            f"Their goal is to {goal}. "
            "Include 5 workout days and 2 rest days. "
            "Each day should have a short description using beginner-friendly language."
        )

        # Create the model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Call the model
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"Unable to generate plan. Error: {e}"



# print(genai_fitness_plan(
#     height="5'8",
#     weight=160,
#     goal="Gain weight",
#     age=22,
#     gender="female"
# ))



def get_recipes(url, params):
    response = requests.get(url,params=params)
    return response.json()


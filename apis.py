import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.environ.get("GENAI_KEY"))



def genai_fitness_plan(height, weight, goal, age=None, gender=None):
    try:
        user_desc = f"someone who is {height} tall, weighs {weight} lbs"
        if age:
            user_desc += f", {age} years old"
        if gender:
            user_desc += f", {gender}"

        prompt = (
            "You are a certified fitness coach and skilled web formatter. "
            "Generate a 1-week beginner-friendly workout plan based on the user's fitness stats and goal. "
            "Avoid technical jargon and use clear, motivating language.\n\n"

            f"User profile: {user_desc}. Their fitness goal is to {goal}.\n\n"

            "Format the output as clean HTML with the following structure:\n"
            "1. Title: Use <h2><strong>Your 1-Week " + goal.capitalize() + " Workout Plan</strong></h2>\n"
            "2. Add a short introductory paragraph.\n"
            "3. For each day (Day 1 to Day 7), use <h3>Day X - [Workout Focus]</h3>\n"
            "4. Under each day, list exercises as HTML <ul> elements:\n"
            "   - Exercise name in <strong>\n"
            "   - 1-2 sentence description\n"
            "   - Add a YouTube search link in this format:\n"
            "     <a href=\"https://www.youtube.com/results?search_query=how+to+[exercise name]\" target=\"_blank\">Watch tutorial</a>\n"
            "5. Add a rest day note for appropriate days (like Day 4).\n"
            "6. End with a motivational tip.\n\n"

            "Make the HTML clean and mobile-friendly. Do not include <html>, <head>, any words that say html in the text or in the headers, or <body> tags—just content ready for insertion in a template."
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text

        # Define images
        exercise_images = {
            "squats": "static/images/squat-exercise-illustration.jpg",
            "push-ups": "static/images/push-up-exercise-illustration.jpg",
            "plank": "static/images/plank-exercise-illustration.jpg",
            "lunges": "static/images/lunges-exercise-illustration.jpg",
            "crunches": "static/images/crunches-exercise-illustration.jpg",
            "jumping jacks": "static/images/jumping-jacks-exercise-illustration.jpg",
        }

        # Inject image tags directly into the HTML content
        for ex, img_path in exercise_images.items():
            img_tag = f'<br><img src="/{img_path}" alt="{ex}" width="250" class="mb-3">'
            # Inject image right after the <strong> tag for the exercise name
            text = text.replace(f"<strong>{ex}</strong>", f"<strong>{ex}</strong>{img_tag}")
            # Handle capitalized versions too
            text = text.replace(f"<strong>{ex.title()}</strong>", f"<strong>{ex.title()}</strong>{img_tag}")

        return {"plan": text, "images": []}

    except Exception as e:
        print("Error generating workout plan:", e)
        return {"plan": "There was an error creating your plan.", "images": []}


# print(genai_fitness_plan(
#     height="5'8",
#     weight=160,
#     goal="Gain weight",
#     age=22,
#     gender="female"
# ))


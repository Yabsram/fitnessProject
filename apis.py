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

    "Make the HTML clean and mobile-friendly. Do not include <html>, <head>, or <body> tags—just content ready for insertion in a template."
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text.lower()


        used_exercises = []
        for key in exercise_images:
            if key in text:
                used_exercises.append((key, exercise_images[key]))

        return {"plan": text, "images": used_exercises}

    except Exception as e:
        return {"plan": f"Unable to generate plan. Error: {e}", "images": []}

exercise_images = {
    "plank": "https://upload.wikimedia.org/wikipedia/commons/1/1c/US_Navy_030317-N-9403F-001_Sailors_participate_in_a_workout_led_by_the_ship%27s_Explosive_Ordnance_Disposal_%28EOD%29_team_in_the_hanger_bay_aboard_the_aircraft_carrier_USS_Abraham_Lincoln_%28CVN_72%29.jpg",
    "squats": "https://upload.wikimedia.org/wikipedia/commons/8/82/Squats.svg",
    "lunges": "https://upload.wikimedia.org/wikipedia/commons/e/ee/A_day_of_staying_fit_160909-F-RN654-179.jpg",
    "push-ups": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Strength_behind_the_engine_%289063543%29.jpg",
    "crunches": "https://upload.wikimedia.org/wikipedia/commons/3/33/Two_sporty_women_doing_exercise_abdominal_crunches%2C_pumping_a_press_on_floor_in_gym_concept_training.jpg",
    "jumping jacks": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Participants_of_a_Crossfit_Undisclosed_workout_perform_jumping_jacks_at_Al_Udeid_Air_Base_in_Qatar_Jan._8%2C_2014_140108-F-AM664-001.jpg"
}

# print(genai_fitness_plan(
#     height="5'8",
#     weight=160,
#     goal="Gain weight",
#     age=22,
#     gender="female"
# ))


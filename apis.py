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
            "You are a certified fitness coach who creates motivating, beginner friendly workout plans "
            "based on people's body stats and fitness goals. Avoid jargon.\n\n"
            f"Create a simple 1-week beginner workout plan for {user_desc}. "
            f"Their goal is to {goal}. "
            "Include 5 workout days and 2 rest days. "
            "Each exercise should be clearly named.\n"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text


        used_exercises = []
        for key in exercise_images:
            if key.lower() in text.lower():
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


# 🏋️ OptiWell — Your AI-Powered Fitness & Wellness Assistant

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from crewai import LLM, Agent, Crew, Task

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ✅ Use Groq's LLaMA 3.3 model with low temperature for consistent advice
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.3 
)

# 🥗 Diet Planner Agent
diet_planner = Agent(
    role="AI Diet Planner",
    goal="Suggest personalized vegetarian diet plans based on user’s fitness goal and weight.",
    backstory="You are a certified nutrition AI helping people plan meals for their health journey.",
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

# 💪 Workout Coach Agent
workout_coach = Agent(
    role="AI Workout Coach",
    goal="Recommend effective daily exercises based on user fitness level and goals.",
    backstory="You are an experienced digital fitness coach who creates safe and effective routines.",
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

# 💧 Hydration Guide Agent
hydration_guide = Agent(
    role="Water Intake Advisor",
    goal="Tell how much water the user should drink based on weight and weather.",
    backstory="You're a hydration expert who helps users stay healthy through optimal water intake.",
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

# 🧠 Motivation Guru Agent
motivation_guru = Agent(
    role="Motivational Coach",
    goal="Send a motivational quote or tip to keep the user on track.",
    backstory="You’re a motivational speaker who supports users with daily fitness motivation.",
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

# 📋 Tasks for each agent
task1 = Task(
    description="User's goal is {goal}, weight is {weight}, and food preference is {food_pref}. Suggest a daily vegetarian diet plan.",
    expected_output="Meal plan for breakfast, lunch, dinner and total calories.",
    agent=diet_planner,
)

task2 = Task(
    description="User is a {fitness_level} with goal of {goal}. Suggest a safe beginner workout routine.",
    expected_output="List of exercises with reps/time and tips.",
    agent=workout_coach,
)

task3 = Task(
    description="User weighs {weight} kg and weather is {weather}. Suggest how much water they should drink today.",
    expected_output="Water intake recommendation in glasses or liters.",
    agent=hydration_guide,
)

task4 = Task(
    description="User is working towards {goal}. Provide a short motivational quote or tip.",
    expected_output="1-line fitness motivation quote or encouragement.",
    agent=motivation_guru,
)

# 👥 Crew
crew = Crew(
    agents=[diet_planner, workout_coach, hydration_guide, motivation_guru],
    tasks=[task1, task2, task3, task4],
    verbose=True
)

# 🚀 Run CLI
result = crew.kickoff(
    inputs={
        "goal": "weight loss",
        "weight": "62",
        "food_pref": "vegetarian",
        "fitness_level": "beginner",
        "weather": "hot"
    }
)

# 🖨️ Final Output
print("\n💪 Final Fitness Plan from OptiWell 💪\n")
print(result)

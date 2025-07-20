import streamlit as st
import os
from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew
from fpdf import FPDF

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)

agents_info = {
    "Diet Planner": {
        "desc": "Personalized meal plans tailored to your preferences",
        "icon": "🥗",
        "agent": Agent(
            role="AI Diet Planner",
            goal="Suggest personalized diet plans based on user’s fitness goal, age, and weight.",
            backstory="You are a certified nutrition AI helping people plan meals for their health journey.",
            allow_delegation=False,
            llm=llm
        )
    },
    "Workout Coach": {
        "desc": "Effective daily workout routines",
        "icon": "🏋️‍♀️",
        "agent": Agent(
            role="AI Workout Coach",
            goal="Recommend effective daily exercises based on user fitness level, goal, and age.",
            backstory="You are an experienced digital fitness coach creating safe and effective routines.",
            allow_delegation=False,
            llm=llm
        )
    },
    "Hydration Guide": {
        "desc": "Optimal water intake recommendations",
        "icon": "💧",
        "agent": Agent(
            role="Water Intake Advisor",
            goal="Tell how much water the user should drink based on weight and weather.",
            backstory="You're a hydration expert who helps users stay healthy through optimal water intake.",
            allow_delegation=False,
            llm=llm
        )
    },
    "Motivation Guru": {
        "desc": "Daily motivational quotes & tips",
        "icon": "✨",
        "agent": Agent(
            role="Motivational Coach",
            goal="Send a motivational quote or tip to keep the user on track.",
            backstory="You’re a motivational speaker who supports users with daily fitness motivation.",
            allow_delegation=False,
            llm=llm
        )
    }
}

st.set_page_config(page_title="OptiWell", page_icon="🌟", layout="wide")

if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "results" not in st.session_state:
    st.session_state.results = {}

# Styles
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    border-radius: 12px;
    color: white;
    animation: slideDown 1s ease;
}
.hero h1 {
    font-size: 3rem;
    margin: 0;
}
.hero p {
    font-size: 1.2rem;
}
.agent-card {
    background: #f5f5f5;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    color: #222222; /* dark text */
}
.agent-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    background: #e0e0e0; /* subtle hover */
}

.agent-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 12px rgba(0,0,0,0.2);
}
.result-box {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    margin-top: 10px;
    color: #000000;
}
@keyframes slideDown {
    from {transform: translateY(-20px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}
            /* 📱 Mobile-friendly tweaks */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  .hero p {
    font-size: 1rem;
  }
  .agent-card {
    margin-bottom: 1rem;
  }
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(
    '<div class="hero"><h1>🌟 OptiWell</h1><p>Your AI-Powered Fitness & Wellness Assistant</p><p>Achieve your health goals with AI!</p></div>',
    unsafe_allow_html=True
)

st.markdown("### 🚀 Let’s start your journey!")

# Form
with st.form("user_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        goal = st.selectbox("🎯 Fitness Goal", [
            "weight loss", "muscle gain", "maintain weight", "weight gain", 
            "endurance", "improve flexibility", "increase stamina", "overall wellness"
        ])
        weight = st.number_input("⚖️ Your Weight (kg)", min_value=30, max_value=200, value=62)
    with col2:
        fitness_level = st.selectbox("💪 Fitness Level", ["beginner", "intermediate", "advanced"])
        food_pref = st.selectbox("🥗 Food Preference", ["vegetarian", "non-vegetarian", "vegan", "eggetarian"])
    with col3:
        weather = st.selectbox("🌤️ Weather", ["hot", "moderate", "cold"])
        age = st.number_input("🎂 Your Age", min_value=10, max_value=100, value=25)

    submitted = st.form_submit_button("✨ Generate Agents")

if submitted:
    st.session_state.user_data = {
        "goal": goal,
        "weight": str(weight),
        "age": str(age),
        "fitness_level": fitness_level,
        "food_pref": food_pref,
        "weather": weather
    }
    st.session_state.results = {}

if st.session_state.user_data:
    st.markdown("## 🌟 Your AI Experts")
    cols = st.columns(4)

    for idx, (agent_name, info) in enumerate(agents_info.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="agent-card">
                <h2>{info['icon']}</h2>
                <h4>{agent_name}</h4>
                <p>{info['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Get advice from {agent_name}", key=agent_name):
                if agent_name == "Diet Planner":
                    task = Task(
                        description=f"User's goal is {st.session_state.user_data['goal']}, weight is {st.session_state.user_data['weight']}, age is {st.session_state.user_data['age']}, and food preference is {st.session_state.user_data['food_pref']}. Suggest a daily diet plan.",
                        expected_output="Meal plan for breakfast, lunch, dinner and total calories.",
                        agent=info["agent"]
                    )
                elif agent_name == "Workout Coach":
                    task = Task(
                        description=f"User is a {st.session_state.user_data['fitness_level']} aged {st.session_state.user_data['age']} with goal of {st.session_state.user_data['goal']}. Suggest a safe workout routine.",
                        expected_output="List of exercises with reps/time and tips.",
                        agent=info["agent"]
                    )
                elif agent_name == "Hydration Guide":
                    task = Task(
                        description=f"User weighs {st.session_state.user_data['weight']} kg and weather is {st.session_state.user_data['weather']}. Suggest how much water they should drink today.",
                        expected_output="Water intake recommendation in glasses or liters.",
                        agent=info["agent"]
                    )
                else:  # Motivation Guru
                    task = Task(
                        description=f"User is working towards {st.session_state.user_data['goal']}. Provide a short motivational quote or tip.",
                        expected_output="1-line fitness motivation quote or encouragement.",
                        agent=info["agent"]
                    )

                crew = Crew(agents=[info["agent"]], tasks=[task], verbose=False)
                result = crew.kickoff(inputs=st.session_state.user_data)
                st.session_state.results[agent_name] = result

            if agent_name in st.session_state.results:
                st.markdown(
                    f"<div class='result-box'><b>{agent_name}:</b><br>{st.session_state.results[agent_name]}</div>",
                    unsafe_allow_html=True
                )

    # PDF Download
    if st.session_state.results:
        if st.button("📄 Download Results as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="OptiWell AI Recommendations", ln=True, align="C")

            for agent, res in st.session_state.results.items():
                pdf.ln(10)
                pdf.multi_cell(0, 10, txt=f"{agent}:\n{res}", align="L")

            pdf_file = "OptiWell_Results.pdf"
            pdf.output(pdf_file)
            with open(pdf_file, "rb") as file:
                st.download_button("⬇️ Download PDF", file, file_name=pdf_file, mime="application/pdf")

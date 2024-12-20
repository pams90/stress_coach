import streamlit as st
import datetime

# Initialize session state for user data
if 'stress_data' not in st.session_state:
    st.session_state['stress_data'] = []

# Function to log stress level
def log_stress(level, timestamp):
    st.session_state['stress_data'].append({'level': level, 'timestamp': timestamp})

# Function to display breathing exercises
def breathing_exercise():
    st.write("### 4-7-8 Breathing Technique")
    st.write("1. Inhale through your nose for 4 seconds.")
    st.write("2. Hold your breath for 7 seconds.")
    st.write("3. Exhale slowly through your mouth for 8 seconds.")
    st.write("4. Repeat for 4 cycles.")

# Function to display mindfulness activity
def mindfulness_activity():
    st.write("### Mindfulness Prompt")
    st.write("Take a moment to observe your surroundings. Note three things you can see, hear, and feel.")

# App layout
st.title("Personalized Stress Management Coach")

# Navigation menu
menu = ["Home", "Breathing Exercises", "Mindfulness Activities", "Log Stress", "Insights"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.write("## Welcome!")
    st.write("Select an option from the menu to begin managing your stress.")

elif choice == "Breathing Exercises":
    st.write("## Breathing Exercises")
    breathing_exercise()

elif choice == "Mindfulness Activities":
    st.write("## Mindfulness Activities")
    mindfulness_activity()

elif choice == "Log Stress":
    st.write("## Log Your Stress Level")
    stress_level = st.slider("How stressed are you feeling right now?", 0, 10, 5)
    if st.button("Log Stress Level"):
        timestamp = datetime.datetime.now()
        log_stress(stress_level, timestamp)
        st.success(f"Stress level {stress_level} logged at {timestamp}.")

elif choice == "Insights":
    st.write("## Your Stress Insights")
    if st.session_state['stress_data']:
        st.write("### Stress Levels Over Time")
        for entry in st.session_state['stress_data']:
            st.write(f"- Level {entry['level']} at {entry['timestamp']}")
    else:
        st.write("No stress data logged yet.")

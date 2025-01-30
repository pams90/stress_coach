import streamlit as st
import datetime
import pandas as pd
import os

# Initialize session state for user data
if 'stress_data' not in st.session_state:
    st.session_state['stress_data'] = []
if 'journal_entries' not in st.session_state:
    st.session_state['journal_entries'] = []

# Function to log stress level
def log_stress(level, timestamp):
    st.session_state['stress_data'].append({'level': level, 'timestamp': timestamp})

# Function to log journal entry
def log_journal(entry, timestamp):
    st.session_state['journal_entries'].append({'entry': entry, 'timestamp': timestamp})

# Function to display breathing exercises
def breathing_exercise():
    st.write("### Breathing Exercises")
    options = {
        "4-7-8 Breathing": ["Inhale through your nose for 4 seconds.", "Hold your breath for 7 seconds.", "Exhale slowly through your mouth for 8 seconds.", "Repeat for 4 cycles."],
        "Box Breathing": ["Inhale through your nose for 4 seconds.", "Hold your breath for 4 seconds.", "Exhale through your mouth for 4 seconds.", "Hold your breath again for 4 seconds.", "Repeat for 4 cycles."],
        "Diaphragmatic Breathing": ["Place one hand on your chest and the other on your stomach.", "Breathe in deeply through your nose, feeling your stomach rise.", "Exhale slowly through pursed lips, feeling your stomach fall.", "Repeat for 5 minutes."]
    }
    exercise = st.selectbox("Choose a breathing exercise:", list(options.keys()))
    st.write("### Instructions:")
    for step in options[exercise]:
        st.write(f"- {step}")

# Function to display mindfulness activities
def mindfulness_activity():
    st.write("### Mindfulness Activities")
    activities = {
        "Gratitude List": "Write down three things you are grateful for today.",
        "Body Scan": "Close your eyes and focus on each part of your body, starting from your toes and moving upward.",
        "5 Senses Exercise": "Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.",
        "Mindful Eating": "Take a small bite of food. Focus on its texture, taste, and smell as you chew slowly."
    }
    activity = st.selectbox("Choose a mindfulness activity:", list(activities.keys()))
    st.write("### Instructions:")
    st.write(activities[activity])

# Function to play background music
import streamlit as st

def play_music():
    st.write("### Background Music")
    music_options = {
        "Meditation Music": [
            "https://github.com/Coding-with-Adam/streamlit-stress-coach/blob/main/music/meditation1.mp3?raw=true",
            "https://github.com/Coding-with-Adam/streamlit-stress-coach/blob/main/music/meditation2.mp3?raw=true"
        ],
        "Relaxing Music": [
            "https://github.com/Coding-with-Adam/streamlit-stress-coach/blob/main/music/relax1.mp3?raw=true",
            "https://github.com/Coding-with-Adam/streamlit-stress-coach/blob/main/music/relax2.mp3?raw=true"
        ]
    }
    music_category = st.selectbox("Choose a music type:", list(music_options.keys()))
    selected_music = st.selectbox("Choose a track:", music_options[music_category])

    try:
        st.audio(selected_music, format="audio/mp3")
    except Exception as e:
        st.error(f"Error playing audio: {e}")
        st.error(f"Selected URL: {selected_music}")
        st.error("Please check the URL is valid and that you are using a supported browser.")

# App layout
st.title("Personalized Stress Management Coach")

# Navigation menu
menu = ["Home", "Breathing Exercises", "Mindfulness Activities", "Log Stress", "Insights", "Journal"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.write("## Welcome to Your Stress Management Coach!")
    st.write("""
        This app provides a collection of tools to help you manage stress, including breathing exercises, mindfulness activities, stress logging, and a journal.
        Navigate using the sidebar menu to get started.
    """)
    st.write("### Get Started")
    st.write("Use the sidebar to select a feature.")


elif choice == "Breathing Exercises":
    st.write("## Breathing Exercises")
    breathing_exercise()
    st.write("### Optional: Play Mindful Background Music")
    play_music()

elif choice == "Mindfulness Activities":
    st.write("## Mindfulness Activities")
    mindfulness_activity()
    st.write("### Optional: Play Mindful Background Music")
    play_music()

elif choice == "Log Stress":
    st.write("## Log Your Stress Level")
    stress_level = st.slider("How stressed are you feeling right now?", 0, 10, 5)
    if st.button("Log Stress Level"):
      if stress_level is not None:
        timestamp = datetime.datetime.now()
        log_stress(stress_level, timestamp)
        st.success(f"Stress level {stress_level} logged at {timestamp}.")
      else:
        st.error("Please select a stress level.")

elif choice == "Insights":
    st.write("## Your Stress Insights")
    if st.session_state['stress_data']:
        st.write("### Stress Levels Over Time")
        # Convert data to a Pandas DataFrame for easy plotting
        df = pd.DataFrame(st.session_state['stress_data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        st.line_chart(df['level'])
    else:
        st.write("No stress data logged yet.")

elif choice == "Journal":
    st.write("## Journal")
    journal_entry = st.text_area("Write your thoughts here:")
    if st.button("Save Entry"):
      if journal_entry:
        timestamp = datetime.datetime.now()
        log_journal(journal_entry, timestamp)
        st.success("Journal entry saved.")
      else:
        st.error("Please add a journal entry.")
    st.write("### Past Entries")
    if st.session_state['journal_entries']:
        for entry in st.session_state['journal_entries']:
            st.write(f"- {entry['timestamp']}: {entry['entry']}")
    else:
        st.write("No journal entries yet.")

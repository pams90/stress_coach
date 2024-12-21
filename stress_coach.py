import streamlit as st
import datetime

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
def play_music():
    st.write("### Background Music")
    music_options = {
        "Meditation Music": ["https://pixabay.com/music/meditationspiritual-simply-meditation-series-11hz-alpha-binaural-waves-for-relaxed-focus-8028/", "https://pixabay.com/music/meditationspiritual-100-binaurale-beats-pur-theta-waves-4-hz-100-ohne-musik-175107/", "https://pixabay.com/music/100-binaurale-beats-pur-delta-waves-3-hz-100-ohne-musik-200251/", "https://pixabay.com/music/meditationspiritual-new-3-hz-239787/", "https://pixabay.com/music/meditationspiritual-blue-sky-binaural-meditation-191542/"],
        "Binaural Beats for Intelligence": ["https://pixabay.com/music/meditationspiritual-gamma-binaural-beats-enhance-brain-power-relaxing-music-for-study-161763/", "https://pixabay.com/music/meditationspiritual-delta-05-to-4-hz-brainwave-frequencies-222950/", "https://pixabay.com/music/meditationspiritual-binaural-beats-6hz-mind-flow-from-album-quottheta-patternsquot-196990/", "https://example.com/binaural4.mp3"],
        "Gratitude Music": ["https://example.com/gratitude1.mp3", "https://example.com/gratitude2.mp3", "https://example.com/gratitude3.mp3", "https://example.com/gratitude4.mp3", "https://example.com/gratitude5.mp3"],
        "Heal Pituitary Gland Music": ["https://example.com/heal1.mp3", "https://example.com/heal2.mp3", "https://example.com/heal3.mp3", "https://example.com/heal4.mp3", "https://example.com/heal5.mp3"],
        "Relaxing Music": ["https://example.com/relax1.mp3", "https://example.com/relax2.mp3", "https://example.com/relax3.mp3", "https://example.com/relax4.mp3", "https://example.com/relax5.mp3"],
        "Deep Healing Music for Body and Soul": ["https://example.com/deepheal1.mp3", "https://example.com/deepheal2.mp3", "https://example.com/deepheal3.mp3", "https://example.com/deepheal4.mp3", "https://example.com/deepheal5.mp3"],
        "Deep Sleep Music": ["https://example.com/sleep1.mp3", "https://example.com/sleep2.mp3", "https://example.com/sleep3.mp3", "https://example.com/sleep4.mp3", "https://example.com/sleep5.mp3"],
        "Study Music": ["https://example.com/study1.mp3", "https://example.com/study2.mp3", "https://example.com/study3.mp3", "https://example.com/study4.mp3", "https://example.com/study5.mp3"],
        "Relaxation Music": ["https://example.com/relaxation1.mp3", "https://example.com/relaxation2.mp3", "https://example.com/relaxation3.mp3", "https://example.com/relaxation4.mp3", "https://example.com/relaxation5.mp3"],
        "Stress Relieving Music": ["https://example.com/stress1.mp3", "https://example.com/stress2.mp3", "https://example.com/stress3.mp3", "https://example.com/stress4.mp3", "https://example.com/stress5.mp3"]
    }
    music_category = st.selectbox("Choose a music type:", list(music_options.keys()))
    selected_music = st.selectbox("Choose a track:", music_options[music_category])
    st.audio(selected_music, format="audio/mp3")

# App layout
st.title("Personalized Stress Management Coach")

# Navigation menu
menu = ["Home", "Breathing Exercises", "Mindfulness Activities", "Log Stress", "Insights", "Journal"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.write("## Welcome!")
    st.write("Select an option from the menu to begin managing your stress.")

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

elif choice == "Journal":
    st.write("## Journal")
    journal_entry = st.text_area("Write your thoughts here:")
    if st.button("Save Entry"):
        timestamp = datetime.datetime.now()
        log_journal(journal_entry, timestamp)
        st.success("Journal entry saved.")
    st.write("### Past Entries")
    if st.session_state['journal_entries']:
        for entry in st.session_state['journal_entries']:
            st.write(f"- {entry['timestamp']}: {entry['entry']}")
    else:
        st.write("No journal entries yet.")

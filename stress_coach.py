import streamlit as st
import requests
import os

# Flask API URL (Change if needed)
API_URL = "http://localhost:5000"

def get_background_sounds():
    try:
        response = requests.get(f"{API_URL}/background-sounds")
        response.raise_for_status()
        return response.json().get("background_sounds", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching background sounds: {e}")
        return []

def upload_background_file(file):
    try:
        files = {'file': file}
        response = requests.post(f"{API_URL}/upload-background", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error uploading file: {e}")
        return None


def generate_binaural_beat(frequency_left, frequency_right, duration, background):
    try:
        payload = {
            "frequency_left": frequency_left,
            "frequency_right": frequency_right,
            "duration": duration,
        }
        if background:
             payload["background"] = background


        response = requests.post(f"{API_URL}/generate", json=payload)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating binaural beat: {e}")
        return None

st.title("Binaural Beat Generator")

# Input fields
col1, col2 = st.columns(2)
with col1:
   frequency_left = st.number_input("Left Frequency (Hz)", min_value=20, max_value=2000, value=200, step=1)
with col2:
   frequency_right = st.number_input("Right Frequency (Hz)", min_value=20, max_value=2000, value=210, step=1)

duration = st.number_input("Duration (seconds)", min_value=1, max_value=3600, value=30, step=1)


# Background Sound
background_options = get_background_sounds()
background_options = ["None"] + background_options
selected_background = st.selectbox("Background Sound", options=background_options)

# Upload Background
uploaded_file = st.file_uploader("Upload Background Sound (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file:
    if st.button("Upload Audio File"):
        upload_response = upload_background_file(uploaded_file)
        if upload_response:
           st.success(f"File uploaded successfully")
           background_options = get_background_sounds()
           background_options = ["None"] + background_options
           selected_background = st.selectbox("Background Sound", options=background_options, index=0) # Reset selection


# Generate Audio button
if st.button("Generate Binaural Beat"):
    background = selected_background if selected_background != "None" else None

    with st.spinner("Generating audio..."):
        audio_bytes = generate_binaural_beat(frequency_left, frequency_right, duration, background)

    if audio_bytes:
        st.audio(audio_bytes, format="audio/mpeg")
        st.success("Binaural beat generated!")

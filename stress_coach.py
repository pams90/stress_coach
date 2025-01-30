from flask import Flask, request, jsonify, send_file
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import io
import os

app = Flask(__name__)

# Ensure directories exist
os.makedirs("background_sounds", exist_ok=True)
os.makedirs("user_backgrounds", exist_ok=True)

# Helper function to generate binaural beats
def generate_binaural_beats(frequency_left, frequency_right, duration_seconds, background=None):
    sample_rate = 44100
    duration = duration_seconds * 1000

    # Create left and right channels
    left = Sine(frequency_left).to_audio_segment(duration=duration)
    right = Sine(frequency_right).to_audio_segment(duration=duration)

    # Combine into stereo sound
    stereo_sound = AudioSegment.from_mono_audiosegments(left, right)

    # Mix with background sound if provided
    if background:
        background_sound = AudioSegment.from_file(background)
        background_sound = background_sound[:duration]  # Match duration
        stereo_sound = stereo_sound.overlay(background_sound)

    return stereo_sound

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        frequency_left = float(data.get("frequency_left", 200))
        frequency_right = float(data.get("frequency_right", 210))
        duration = int(data.get("duration", 30))
        background = data.get("background")

        if not (20 <= frequency_left <= 2000 and 20 <= frequency_right <= 2000):
            return jsonify({"error": "Frequencies must be between 20 and 2000 Hz"}), 400
        if not (1 <= duration <= 3600):
            return jsonify({"error": "Duration must be between 1 and 3600 seconds"}), 400

        background_path = None
        if background:
            background_path = os.path.join("background_sounds", background) if background in os.listdir("background_sounds") else os.path.join("user_backgrounds", background)
            if not os.path.exists(background_path):
                return jsonify({"error": "Background sound not found"}), 400

        audio = generate_binaural_beats(frequency_left, frequency_right, duration, background_path)

        buffer = io.BytesIO()
        audio.export(buffer, format="mp3")
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name="binaural_beat.mp3", mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-background', methods=['POST'])
def upload_background():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400

        if file.mimetype not in ['audio/mpeg', 'audio/wav']:
            return jsonify({"error": "Only MP3 and WAV formats are supported"}), 400

        if len(file.read()) > 10 * 1024 * 1024:  # 10 MB size limit
            return jsonify({"error": "File size exceeds 10 MB limit"}), 400

        file.seek(0)  # Reset file pointer
        save_path = os.path.join("user_backgrounds", file.filename)
        file.save(save_path)

        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

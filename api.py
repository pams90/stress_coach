from flask import Flask, request, jsonify, send_file
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import io
import os
import uuid # Import uuid library

app = Flask(__name__)

# Ensure directories exist
os.makedirs("background_sounds", exist_ok=True)
os.makedirs("user_backgrounds", exist_ok=True)

def generate_download_name(frequency_left, frequency_right):
     return f"binaural_beat_{frequency_left}Hz_{frequency_right}Hz.mp3"

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

        download_name = generate_download_name(frequency_left, frequency_right)

        return send_file(buffer, as_attachment=True, download_name=download_name, mimetype="audio/mpeg")
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

        # File size check before reading content into memory
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0) # Reset to the beginning after checking the size
        if file_size > 10 * 1024 * 1024:  # 10 MB size limit
            return jsonify({"error": "File size exceeds 10 MB limit"}), 400

        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        save_path = os.path.join("user_backgrounds", unique_filename)
        file.save(save_path)

        return jsonify({"message": "File uploaded successfully", "filename": unique_filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/background-sounds', methods=['GET'])
def get_background_sounds():
    try:
        background_files = os.listdir("background_sounds") + os.listdir("user_backgrounds")
        return jsonify({"background_sounds": background_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask API server...")
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)

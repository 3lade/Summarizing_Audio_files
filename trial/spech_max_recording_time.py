import os
import threading
import speech_recognition as sr
from summarizer import Summarizer

# Create a recognizer instance
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Define the data folder path where you want to save files
data_folder = 'without\\data\\download_from_microphone'

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Initialize an audio file name and recording state
audio_file_path = None
recording = False

# Define the maximum recording duration (in seconds)
max_recording_duration = 60

# Timer to track inactivity
inactivity_timer = None

# Function to handle inactivity timeout and stop recording
def handle_inactivity():
    global recording
    if recording:
        print("Recording stopped due to inactivity.")
        stop_recording()

# Function to start recording
def start_recording():
    global recording, audio_file_path, inactivity_timer
    print("Recording started.")
    audio_file_path = os.path.join(data_folder, "audio.wav")
    with open(audio_file_path, "wb") as audio_file:
        recording = True
        inactivity_timer = threading.Timer(max_recording_duration, handle_inactivity)
        inactivity_timer.start()
        audio_file.write(recognizer.listen(microphone, timeout=max_recording_duration).get_wav_data())

# Function to stop recording
def stop_recording():
    global recording, inactivity_timer
    recording = False
    if inactivity_timer:
        inactivity_timer.cancel()
        inactivity_timer = None
    summarized_text = summarize_audio(audio_file_path)
    save_summarized_text(audio_file_path, summarized_text)
    print(f"Recording stopped. Audio saved as '{audio_file_path}'.")

# Function to summarize audio
def summarize_audio(audio_file):
    model = Summarizer()
    audio_text = ""
    try:
        with open(audio_file, "rb") as audio_file:
            audio_text = audio_file.read().decode("utf-8")
    except Exception as e:
        print(f"Error reading audio file: {str(e)}")
    summary = model(audio_text)
    return summary

# Function to save summarized text to a file
def save_summarized_text(audio_file, text):
    summary_file = os.path.splitext(audio_file)[0] + "_summary.txt"
    with open(summary_file, "w") as f:
        f.write(text)

# Start listening for commands
print("Listening... Say 'start recording' to begin and recording will stop after 60 seconds of inactivity.")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    while True:
        audio = recognizer.listen(source, timeout=None)
        try:
            recognized_text = recognizer.recognize_google(audio)
            if "start recording" in recognized_text.lower():
                start_recording()
            else:
                if recording:
                    with open(audio_file_path, "ab") as audio_file:
                        audio_file.write(audio.get_wav_data())
                        if inactivity_timer:
                            inactivity_timer.cancel()
                            inactivity_timer = threading.Timer(max_recording_duration, handle_inactivity)
                            inactivity_timer.start()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

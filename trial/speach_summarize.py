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

# Function to start recording
def start_recording():
    global recording, audio_file_path
    print("Recording started.")
    audio_file_path = os.path.join(data_folder, "audio.wav")
    with open(audio_file_path, "wb") as audio_file:
        recording = True
        audio_file.write(recognizer.listen(microphone).get_wav_data())

# Function to stop recording
def stop_recording():
    global recording
    if recording:
        recording = False
        print("Recording stopped.")
        summarized_text = summarize_audio(audio_file_path)
        save_summarized_text(audio_file_path, summarized_text)
        print(f"Audio saved as '{audio_file_path}'.")
    else:
        print("Recording is not active. Say 'start recording' to begin.")

# Function to summarize audio
def summarize_audio(audio_file):
    model = Summarizer()
    audio_text = ""
    try:
        with open(audio_file, "rb") as audio_file:
            audio_text = audio_file.read().decode("utf-8", errors='ignore')
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
print("Listening... Say 'start recording' to begin and 'end recording' to stop.")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    while True:
        audio = recognizer.listen(source, timeout=None)
        try:
            recognized_text = recognizer.recognize_google(audio)
            if "start recording" in recognized_text.lower():
                start_recording()
            elif "end recording" in recognized_text.lower():
                stop_recording()
            else:
                if recording:
                    with open(audio_file_path, "ab") as audio_file:
                        audio_file.write(audio.get_wav_data())
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

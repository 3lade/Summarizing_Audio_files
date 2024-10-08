import pyaudio
import wave
import threading
import speech_recognition as sr
from summarizer import Summarizer

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILENAME = "audio.wav"
END_PHRASE = "end recording"

# Initialize audio recording
audio_frames = []
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Function to save audio data to a file
def save_audio(filename, audio_data):
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(audio_data))
    wf.close()

# Function to summarize text
def summarize_text(text):
    model = Summarizer()
    summary = model(text)
    return summary

# Thread for real-time audio recording
def audio_thread():
    print(f"Listening... Speak '{END_PHRASE}' to stop.")
    while True:
        audio_data = stream.read(CHUNK)
        audio_frames.append(audio_data)
        text = transcribe_audio()
        if text and END_PHRASE in text.lower():
            print("Recording stopped. Audio saved as 'audio.wav'.")
            save_audio(AUDIO_FILENAME, audio_frames)
            break

# Function to transcribe audio using CMU Sphinx
def transcribe_audio():
    recognizer = sr.Recognizer()
    audio_data = b"".join(audio_frames)
    audio_source = sr.AudioData(audio_data, RATE, audio.get_sample_size(FORMAT))
    try:
        text = recognizer.recognize_sphinx(audio_source)
        return text
    except sr.UnknownValueError:
        return None

# Start the audio recording thread
audio_recording_thread = threading.Thread(target=audio_thread)
audio_recording_thread.start()

# Main thread for summarization
audio_recording_thread.join()  # Wait for audio recording to finish

# Summarize the recorded audio
transcribed_text = transcribe_audio()
if transcribed_text:
    summary = summarize_text(transcribed_text)
    if summary:
        print("Summary:")
        print(summary)
    else:
        print("Summary generation failed.")
else:
    print("No speech detected or transcription failed.")

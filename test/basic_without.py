import os

import speech_recognition as sr
from summarizer import Summarizer


# Function to transcribe audio using Google Web Speech API
def transcribe_audio(audio_clip):
    recognizer = sr.Recognizer()
    with audio_clip as source:
        audio = recognizer.record(source)

    try:
        transcribed_text = recognizer.recognize_google(audio)
        return transcribed_text
    except sr.UnknownValueError:
        return "Transcription failed: Could not understand audio"
    except sr.RequestError:
        return "Transcription failed: Could not request results"

# Function to summarize text using BERT extractive summarizer
def summarize_text(text):
    model = Summarizer()
    summary = model(text)
    return summary

# Main function
def main():
    audio_file_path = "path/to/your/local/audio.mp3"  # Replace with the path to your local audio file

    # Load the audio from the local file
    audio_clip = sr.AudioFile(audio_file_path)

    # Transcribe the loaded audio
    transcribed_text = transcribe_audio(audio_clip)

    # Summarize the transcribed text
    summary = summarize_text(transcribed_text)

    # Print the summary
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()

import os
import tempfile

import moviepy.editor as mp
import requests
import speech_recognition as sr
from pytube import YouTube
from summarizer import Summarizer


# Function to download audio from a YouTube video URL
def download_audio_from_youtube(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    return stream.download()

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
    video_url = input("Enter the YouTube video URL: ")
    
    # Download audio from the YouTube video URL
    audio_file = download_audio_from_youtube(video_url)

    # Extract audio from the downloaded file
    audio = mp.AudioFileClip(audio_file)

    # Transcribe the extracted audio
    transcribed_text = transcribe_audio(audio)

    # Summarize the transcribed text
    summary = summarize_text(transcribed_text)

    # Print the summary
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()

import os
import moviepy.editor as mp
import speech_recognition as sr
from summarizer import Summarizer
from pytube import YouTube

def download_video_audio(video_url, video_directory):
    try:
        # Download the YouTube video using pytube
        yt = YouTube(video_url)
        yt.streams.filter(only_audio=True).first().download(output_path=video_directory, filename="audio.mp4")
        return os.path.join(video_directory, "audio.mp4")
    except Exception as download_error:
        print("Error while downloading the video:", download_error)
        return None

def convert_audio_to_wav(audio_file, video_directory):
    try:
        output_audio_file = os.path.join(video_directory, "audio.wav")
        clip = mp.AudioFileClip(audio_file)
        clip.write_audiofile(output_audio_file)
        return output_audio_file
    except Exception as conversion_error:
        print("Error while converting audio:", conversion_error)
        return None

def transcribe_audio_to_text(audio_file):
    try:
        audio_file = os.path.join(video_directory, "audio.wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return  recognizer.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        return "Unable to transcribe audio - No speech detected."
    except sr.RequestError as recognition_error:
        return f"Recognition request failed: {recognition_error}"

def summarize_text(text):
    try:
        summarizer = Summarizer()
        return summarizer(text)
    except Exception as summarization_error:
        return f"Error during summarization: {summarization_error}"

def save_summary_to_file(summary, output_directory):
    summary_file = os.path.join(output_directory, "summary.txt")
    try:
        with open(summary_file, "w") as output_file:
            output_file.write(summary)
        return summary_file
    except Exception as save_error:
        print("Error while saving the summary:", save_error)
        return None

# Define the directories for files
video_directory = "without\\data\\download_from_url"
output_directory = "without\\data\\output"

# Check if the directories exist and create them if not
if not os.path.exists(video_directory):
    os.makedirs(video_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Step 1: Get video URL from the user
video_url = input("Enter the YouTube video URL: ")

# Step 2: Download video audio
downloaded_audio_file = download_video_audio(video_url, video_directory)

# Step 3: Convert audio to WAV
if downloaded_audio_file:
    output_audio_file = convert_audio_to_wav(downloaded_audio_file, video_directory)
else:
    output_audio_file = None

# Step 4: Transcribe audio to text
if output_audio_file:
    transcribed_text = transcribe_audio_to_text(output_audio_file)
else:
    transcribed_text = None

# Step 5: Summarize the transcribed text
summary = summary_file = None
if transcribed_text:
    summary = summarize_text(transcribed_text)
    
# Step 6: Save the summary to a file
if summary:
    summary_file = save_summary_to_file(summary, output_directory)

print("Audio saved as:", output_audio_file)
if summary_file:
    print("Summary saved to:", summary_file)

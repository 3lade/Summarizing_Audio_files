import os
import moviepy.editor as mp
import speech_recognition as sr
from summarizer import Summarizer

# Define the directories for files
video_directory = "without\\data"
output_directory = "without\\data"

# Check if the directories exist and create them if not
if not os.path.exists(video_directory):
    os.makedirs(video_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Step 1: Convert video to audio
video_file = os.path.join(video_directory, "Mojo.mp4")
audio_file = os.path.join(output_directory, "output_audio.wav")

clip = mp.VideoFileClip(video_file)
clip.audio.write_audiofile(audio_file)

# Step 2: Transcribe audio to text
recognizer = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio = recognizer.record(source)
transcribed_text = recognizer.recognize_google(audio)

# Step 3: Summarize the transcribed text
summarizer = Summarizer()
summary = summarizer(transcribed_text)

# Output the summary
summary_file = os.path.join(output_directory, "summary_mojo.txt")
with open(summary_file, "w") as output_file:
    output_file.write(summary)

print("Summary saved to:", summary_file)

import os
from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
from summarizer import Summarizer

# Function to create a directory if it doesn't exist
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download audio from a YouTube video URL
def download_audio_from_youtube(video_url, save_path):
    create_directory_if_not_exists(save_path)  # Create the directory if it doesn't exist
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_file = os.path.join(save_path, "download_for_url", "audio.mp4")  # Save as a file
    stream.download(output_path=os.path.join(save_path, "download_for_url"), filename="audio")
    return audio_file

# Function to convert audio to the desired format
def convert_audio_format(input_audio, output_audio, file_extension):
    audio = mp.AudioFileClip(input_audio)
    audio.write_audiofile(output_audio, codec=file_extension)

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
    
    # Define the data folder and file paths using double backslashes
    data_folder = "C:\\Users\\Sivamani\\OneDrive\\Desktop\\Summarizing Audio Files in Python\\without\\data"
    
    # Create the data folder if it doesn't exist
    create_directory_if_not_exists(data_folder)
    
    # Download audio from the YouTube video URL
    audio_file_path = download_audio_from_youtube(video_url, data_folder)

    # Check if audio file is successfully downloaded
    if audio_file_path:
        # Specify the desired file extension (e.g., "mp3" or "wav")
        desired_extension = "mp3"

        # Convert audio to the desired format
        converted_audio_file = os.path.join(data_folder, "download_for_url", "audio." + desired_extension)
        convert_audio_format(audio_file_path, converted_audio_file, desired_extension)

        # Transcribe the extracted audio
        audio = mp.AudioFileClip(converted_audio_file)
        transcribed_text = transcribe_audio(audio)

        # Summarize the transcribed text
        summary = summarize_text(transcribed_text)

        # Print the summary
        print("Summary:")
        print(summary)

    else:
        print("Audio download failed. Check the video URL and your internet connection.")

if __name__ == "__main__":
    main()

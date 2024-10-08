import os

import moviepy.editor as mp
import speech_recognition as sr
import youtube_dl
from summarizer import Summarizer


def download_youtube_video(url, save_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_path, "video.%(ext)s"),
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
        return os.path.join(save_path, f"video.{info_dict['ext']}")
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

def extract_audio(video_file, audio_file):
    try:
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file, codec='pcm_s16le', audio_fps=44100)  # Specify codec and audio FPS
        video.close()
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")

def transcribe_audio(audio_file):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return None

def summarize_text(text):
    try:
        model = Summarizer()
        summary = model(text)
        return summary
    except Exception as e:
        print(f"Error summarizing text: {str(e)}")
        return None

if __name__ == "__main__":
    # Define the YouTube video URL you want to process
    video_url = "https://youtu.be/cJt68xkbO6U?feature=shared"

    # Define the data folder and file paths using double backslashes
    data_folder = "without\\data\\video"
    
    # Create the data folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    # Download the YouTube video and get the video file path
    video_file_path = download_youtube_video(video_url, data_folder)

    if video_file_path:
        # Define the audio file path
        audio_file_path = os.path.join(data_folder, "audio.wav")

        # Extract audio from the video
        extract_audio(video_file_path, audio_file_path)

        # Transcribe the audio to text
        transcribed_text = transcribe_audio(audio_file_path)

        if transcribed_text:
            # Summarize the transcribed text
            summary = summarize_text(transcribed_text)
            
            if summary:
                # Print or save the summary as needed
                print(summary)
            else:
                print("Summary generation failed.")
        else:
            print("Transcription failed. Check the audio file for issues.")
    else:
        print("Video download failed. Check the video URL and your internet connection.")

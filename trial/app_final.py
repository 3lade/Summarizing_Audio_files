import os
from flask import Flask, render_template, request, redirect, url_for
from summarizer import Summarizer
import subprocess
import youtube_dl
import moviepy.editor as mp
import speech_recognition as sr
from pytube import YouTube

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'without\\uploads'# Define the folder for file uploads

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def download_video_audio(video_url, video_directory):
    try:
        # Download the YouTube video using pytube
        yt = YouTube(video_url)
        yt.streams.filter(only_audio=True).first().download(output_path=video_directory, filename="vedio.mp4")
        return os.path.join(video_directory, "vedio.mp4")
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
    
def extract_audio(video_file, output_path):
    try:
        video = mp.VideoFileClip(video_file)
        
        # Check if the video has a valid fps
        if video.fps is None:
            raise Exception("Invalid video fps")
        
        audio = video.audio
        audio_file = os.path.join(output_path, "audio.wav")
        vedio.write_audiofile(audio_file)
        video.close()
        return audio_file
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None
    
def transcribe_audio(audio_file):
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' does not exist.")
        return None

    # Check the format of the audio file and convert it to WAV if needed
    audio_format = audio_file.split('.')[-1]
    if audio_format != 'wav':
        try:
            # Convert the audio file to WAV format
            output_audio_file = audio_file.replace(audio_format, 'wav')
            audio = mp.AudioFileClip(audio_file)
            audio.write_audiofile(output_audio_file, codec='pcm_s16le')  # Use 'pcm_s16le' codec for WAV format
            audio.close()
            audio_file = output_audio_file
        except Exception as e:
            print(f"Error converting audio to WAV format: {str(e)}")
            return None

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language="en-US")
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
    
def save_transcribed_text(transcribed_text):
    text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transcribed_text.txt')
    with open(text_file_path, 'w') as text_file:
        text_file.write(transcribed_text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/summarize_video_audio', methods=['POST'])
def summarize_video_audio():
    # Return the summary as a string
    data_folder = "without\\data\\download_for_url"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    youtube_url = request.form['youtube_url']
    video_file_path = download_video_audio(youtube_url, data_folder)

    if video_file_path:
        audio_file_path = os.path.join(data_folder, "audio")

        extracted_audio_file = convert_audio_to_wav(video_file_path, data_folder)
        if extracted_audio_file:
            transcribed_text = transcribe_audio(extracted_audio_file)

            if transcribed_text:
                summary = summarize_text(transcribed_text)

                if summary:
                    return summary
                else:
                    return "Summary generation failed."
            else:
                return "Transcription failed. Check the audio file for issues."
        else:
            return "Audio conversion failed."
    else:
        return "Video download failed. Check the video URL and your internet connection."

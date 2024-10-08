import os
from flask import Flask, render_template, request
from summarizer import Summarizer
import moviepy.editor as mp
import speech_recognition as sr
from pytube import YouTube

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define the folder for file uploads

# Ensure the "uploads" folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def download_video_audio(video_url, video_directory):
    try:
        # Download the YouTube video using pytube
        yt = YouTube(video_url)
        yt.streams.filter(only_audio=True).first().download(output_path=video_directory, filename="video.mp4")
        return os.path.join(video_directory, "video.mp4")
    except Exception as download_error:
        print("Error while downloading the video:", download_error)
        return None

def transcribe_audio(audio_file):
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

# Summarize microphone audio
def summarize_microphone_audio():
    try:
        # Record audio from the microphone
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source)

        # Transcribe the recorded audio
        audio_text = recognizer.recognize_google(audio)
        if audio_text:
            summary = summarize_text(audio_text)
            if summary:
                return summary
            else:
                return "Summary generation failed."
        else:
            return "No speech detected."
    except sr.RequestError as e:
        return f"Could not request results: {str(e)}"
    except sr.UnknownValueError:
        return "No speech detected."


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize_video_audio', methods=['POST'])
def summarize_video_audio():
    data_folder = "data/download_for_url"
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    youtube_url = request.form['youtube_url']
    video_file_path = download_video_audio(youtube_url, data_folder)

    if video_file_path:
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(video_file_path) as source:
                audio = recognizer.record(source)
            audio_text = recognizer.recognize_google(audio, language="en-US")

            if audio_text:
                summary = summarize_text(audio_text)
                if summary:
                    return summary
                else:
                    return "Summary generation failed."
            else:
                return "Transcription failed. Check the audio file for issues."
        except sr.RequestError as e:
            return f"Could not request results: {str(e)}"
    else:
        return "Video download failed. Check the video URL and your internet connection."

@app.route('/summarize_microphone_audio', methods=['POST'])
def summarize_microphone_audio_route():
    result = summarize_microphone_audio()
    return result

@app.route('/summarize_file_audio', methods=['POST'])
def summarize_file_audio():
    uploaded_file = request.files['video_upload']  # Get the uploaded file

    if uploaded_file:
        # Save the uploaded file to the "uploads" folder
        video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(video_file_path)

        # Process the uploaded video file
        if video_file_path:
            data_folder = "without\\data\\download_for_url"
            
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            extracted_audio_file = extract_audio(video_file_path, data_folder)

            if extracted_audio_file:
                transcribed_text = transcribe_audio(extracted_audio_file)

                if transcribed_text:
                    # Save the transcribed text
                    save_transcribed_text(transcribed_text)
                    summary = summarize_text(transcribed_text)

                    if summary:
                        return summary
                    else:
                        return "Summary generation failed."
                else:
                    return "Transcription failed. Check the audio file for issues."
            else:
                return "Audio extraction failed."
        else:
            return "Video processing failed. Check the uploaded file."
    else:
        return "No file uploaded."

if __name__ == "__main__":
    app.run(debug=True)

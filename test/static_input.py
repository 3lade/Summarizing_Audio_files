import os
import subprocess

import speech_recognition as sr


def extract_audio(video_file, output_audio):
    # Define the FFmpeg command to extract audio
    cmd = [
        "ffmpeg", 
        "-i", video_file, 
        "-vn", 
        "-acodec", "pcm_s16le", 
        "-ar", "44100", 
        "-ac", "2", 
        output_audio
    ]
    
    try:
        # Run the FFmpeg command
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def main():
    video_file = r'C:\Users\Sivamani\OneDrive\Desktop\Summarizing Audio Files in Python\Without\Mojo.mp4'
    audio_file = "audio.wav"

    # Extract audio from the video
    if extract_audio(video_file, audio_file):
        print("Audio extraction and transcription successful.")
        transcribed_text = transcribe_audio(audio_file)
        print(transcribed_text)
        os.remove(audio_file)  # Remove the temporary audio file
    else:
        print("Audio extraction failed.")

if __name__ == "__main__":
    main()

import os
import threading
from googletrans import Translator
import speech_recognition as sr
from summarizer import Summarizer

# Create a recognizer instance
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Create a translator instance
translator = Translator()

# Initialize the summarizer
model = Summarizer()

# Function to summarize text
def summarize_text(text):
    summary = model(text)
    return summary

# Function to transcribe, translate, and summarize audio
def transcribe_translate_summarize_audio():
    with microphone as source:
        audio = recognizer.listen(source)
        try:
            # Transcribe the audio
            transcribed_text = recognizer.recognize_google(audio, language='en')
            
            # Translate the transcribed text to English
            translated_text = translator.translate(transcribed_text, src='te', dest='en')  # 'te' is for Telugu
            
            # Summarize the translated text
            summary = summarize_text(translated_text.text)

            if summary:
                print("Summary:")
                print(summary)
            else:
                print("Summary generation failed.")
        except sr.UnknownValueError:
            print("No speech detected.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

# Start listening for audio
print("Listening... Say something in Telugu.")
transcribe_translate_summarize_audio()

from gtts import gTTS

# Path to the summary text file
summary_file_path =  r'without\data\download_for_url\summary.txt'

# Read the summary text from the file
with open(summary_file_path, 'r', encoding='utf-8') as file:
    summary_text = file.read()

# Create a gTTS object and convert the summary text to speech
tts = gTTS(text=summary_text, lang='en')  # Language is set to English (en)
tts.save('without\data\download_for_url\summary_audio.mp3')  # Save the audio to a file (e.g., summary_audio.mp3)

import json
import os
import time

import moviepy.editor as mp
import requests

# Replace with your AssemblyAI API token
ASSEMBLYAI_API_TOKEN = "YOUR_API_TOKEN"

# Function to extract audio from a video link
def extract_audio_from_video_link(video_link):
    video = mp.VideoFileClip(video_link)
    audio = video.audio
    return audio

# Function to transcribe audio using AssemblyAI API
def transcribe_audio(audio_file):
    # AssemblyAI transcript endpoint (where we submit the audio file)
    transcript_endpoint = "https://api.assemblyai.com/v2/upload"

    # Request parameters
    data = {
        "audio_url": audio_file
    }

    # HTTP request headers
    headers = {
        "authorization": ASSEMBLYAI_API_TOKEN,
        "content-type": "application/json"
    }

    # Submit audio for transcription via HTTP request
    response = requests.post(transcript_endpoint, json=data, headers=headers)

    if response.status_code == 201:
        transcript_id = response.json()["id"]
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

        # Polling for transcription completion
        while True:
            transcription_result = requests.get(polling_endpoint, headers=headers).json()

            if transcription_result['status'] == 'completed':
                # Print the results
                print("Transcription completed.")
                return transcription_result['text']
            elif transcription_result['status'] == 'failed':
                raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
            else:
                time.sleep(3)
    else:
        raise RuntimeError(f"Transcription request failed with status code {response.status_code}")

# Function to summarize text using AssemblyAI API
def summarize_text(text):
    # AssemblyAI summarize endpoint
    summarize_endpoint = "https://api.assemblyai.com/v2/summarize"

    # Request parameters
    data = {
        "text": text,
        "num_sentences": 3  # Adjust the number of sentences in the summary as needed
    }

    # HTTP request headers
    headers = {
        "authorization": ASSEMBLYAI_API_TOKEN,
        "content-type": "application/json"
    }

    # Submit text for summarization via HTTP request
    response = requests.post(summarize_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        summary = response.json()["summary"]
        return summary
    else:
        raise RuntimeError(f"Summarization request failed with status code {response.status_code}")

# Main function
def main():
    video_link = input("Enter the video link: ")
    audio_file = extract_audio_from_video_link(video_link)
    text_file = "data/extracted_text.txt"

    # Transcribe the extracted audio
    transcribed_text = transcribe_audio(audio_file)

    # Save the transcribed text to a file
    with open(text_file, "w") as f:
        f.write(transcribed_text)

    # Summarize the text and print the summary
    summary = summarize_text(transcribed_text)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()

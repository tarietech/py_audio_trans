import openai

# Read the API key from the file
with open("pythonai/api.txt", "r") as api_file:
    api_key = api_file.read().strip()

# Set the API key for OpenAI
openai.api_key = api_key

audio_file_path = input("Enter the file path of the audio: ")

with open(audio_file_path, "rb") as audio_file:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

print(transcript)

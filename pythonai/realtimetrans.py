import openai
import pyaudio
import wave
import os
import tempfile

with open("pythonai/api.txt", "r") as api_file:
    api_key = api_file.read().strip()

# Set the API key for OpenAI
openai.api_key = api_key

# Create a temporary WAV file to store audio
temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
temp_audio_file.close()
temp_audio_file_path = temp_audio_file.name

# Initialize audio stream parameters
audio_format = pyaudio.paInt16  # 16-bit audio
channels = 1  # Mono
sample_rate = 16000  # Common sample rate for OpenAI models
chunk_size = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a PyAudio audio stream
stream = audio.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

try:
    print("Recording... (Press Ctrl+C to stop)")
    frames = []

    while True:
        data = stream.read(chunk_size)
        frames.append(data)

except KeyboardInterrupt:
    print("Recording stopped.")

finally:
    print("Closing audio stream...")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Saving audio to a WAV file...")
    with wave.open(temp_audio_file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    print("Transcribing audio...")
    with open(temp_audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print("Transcription:")
    print(transcript)

    # Clean up temporary WAV file
    os.remove(temp_audio_file_path)

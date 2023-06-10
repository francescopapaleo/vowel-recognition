import librosa
import sounddevice as sd
from pythonosc import udp_client
import numpy as np

print(librosa.__version__)

# Initialize OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

sample_rate = 44100
n_fft = 512  # FFT window size
hop_length = 256  # number of samples between successive frames
n_mels = 128  # number of Mel bands

def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Volume norm: {volume_norm}")

    audio_data = indata[:, 0]
    print(f"Audio data shape: {audio_data.shape}")
    print(f"Audio data type: {type(audio_data)}")
    print(f"Audio data first 10 elements: {audio_data[:10]}")

# ------------------- Audio Feature Extraction ------------------- #








# ---------------------------------------------------------------- #

    client.send_message("/wek/inputs", audio_data.flatten().tolist())

# Start the audio stream and capture microphone input
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Audio stream started. Press Ctrl+C to stop.")
    try:
        while True:
            pass  # Keeps the program running until interrupted
    except KeyboardInterrupt:
        print("Audio stream stopped.")
    except Exception as e:
        print(f"Error in audio_callback: {e}")
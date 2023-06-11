import librosa
import sounddevice as sd
from pythonosc import udp_client
import numpy as np

print(librosa.__version__)

sample_rate = 44100

# Initialize OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 6448)


def extract_formants(audio, sample_rate):
    formants = librosa.lpc(audio, order=10)                     # LPC to get LPF coefs
    roots = np.roots(formants) 
    roots = roots[np.imag(roots) >= 0]                          # Only take roots in the upper half-plane
    frequencies = np.arctan2(np.imag(roots), np.real(roots)) \
    * (sample_rate / (2 * np.pi))                               # Convert LPC > frequency
    frequencies = np.sort(frequencies)                          # Sort frequencies in ascending order
    return frequencies[0], frequencies[1], frequencies[2]       # Return the first 3, which are enough to identify the vowel


def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    if status:
        print(f"Status: {status}")
    
    if any(indata):
        # Convert the incoming audio to a NumPy array
        buffer = np.squeeze(indata)
    else:
        print("No input data")

    # Process the current audio frame using librosa
    f1, f2, f3 = extract_formants(buffer, sample_rate)
    
    formants = [float(f1), float(f2), float(f3)] # This line is changed to cast the formants to regular Python float type
    client.send_message("/wek/inputs", formants)


# Query available input devices
input_devices = sd.query_devices()
input_device_name = input_devices[0]["name"]  # Access the first device in the tuple and retrieve the name

# Start the audio stream and capture microphone input
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, device=0):
    print(f"Selected audio device: {input_device_name}")
    print("Audio stream started. Press Ctrl+C to stop.")
    try:
        while True:
            pass  # Keeps the program running until interrupted
    except KeyboardInterrupt:
        print("Audio stream stopped.")
    except Exception as e:
        print(f"Error in audio_callback: {e}")


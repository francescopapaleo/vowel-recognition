# audio-osc.py

import speech_recognition as sr
import numpy as np
from pythonosc import udp_client
from formants import detect_formants

if __name__ == "__main__":
    sample_rate = 44100     
    chunk = 4096

    # Initialize OSC client
    client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

    # Initialize a recognizer object
    r = sr.Recognizer()

    # Open the microphone stream
    with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk) as source:
        while True:
            try:
                # Read the chunk of audio data from the microphone
                audio = r.record(source, duration=chunk / sample_rate)

                # Convert the audio to a numpy array
                audio_data = np.frombuffer(audio.frame_data, np.int16)

                # Add a small constant to the audio data to prevent division by zero
                audio_data = audio_data + 1e-10

                f1, f2, _, _ = detect_formants(audio_data, sample_rate, f0min=200, f0max=3000)

                formants = [float(f1), float(f2)]
                
                # Check if valid formants were returned before sending them to Wekinator
                client.send_message("/wek/inputs", formants)
                
            except KeyboardInterrupt:
                print("Program stopped.")
                
            except Exception as e:
                print(f"Exception: {e}")


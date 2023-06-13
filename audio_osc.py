# audio-osc.py

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

from pythonosc import udp_client
from formants import detect_formants
from matplotlib.animation import FuncAnimation


if __name__ == "__main__":

    sample_rate = 44100     
    frames_per_buffer = 1024

    # Initialize OSC client 
    client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

    mic = pyaudio.PyAudio()

    audio_input = mic.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=44100, 
                input=True, 
                frames_per_buffer=frames_per_buffer)

    try:
    
        while True:
            buffer = np.frombuffer(audio_input.read(frames_per_buffer), dtype=np.int16)
            
            formants = detect_formants(
                buffer, sample_rate, frames_per_buffer, f0min=150, f0max=500)

            formants = [val if not np.isnan(val) else 0.0 for val in formants]
    
            client.send_message("/wek/inputs", formants)
            
    except KeyboardInterrupt:
        print("Program stopped.")
    audio_input.stop_stream()
    audio_input.close()
    mic.terminate()


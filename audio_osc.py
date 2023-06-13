# audio-osc.py

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

from pythonosc import udp_client
from formants import detect_formants
from matplotlib.animation import FuncAnimation

if __name__ == "__main__":
    # OSC settings
    ip_address = "127.0.0.1"
    port = 6448

    sample_rate = 48000
    frames_per_buffer = 4096
    f0min = 150
    f0max = 5000

    # Initialize OSC client 
    client = udp_client.SimpleUDPClient(ip_address, port)

    audio = pyaudio.PyAudio()

    audio_input = audio.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=sample_rate, 
                input=True, 
                frames_per_buffer=frames_per_buffer)

    try:
        while True:
            buffer = np.frombuffer(audio_input.read(frames_per_buffer), dtype=np.int16)
            
            formants = detect_formants(
                buffer, sample_rate, frames_per_buffer, f0min, f0max)
            print(f"Sending OSC messages to {ip_address}:{port} with values: {formants}", end='\r')
            client.send_message("/wek/inputs", formants)
            
    except KeyboardInterrupt:
        print("Program stopped.")
    finally:
        audio_input.stop_stream()
        audio_input.close()
        audio.terminate()
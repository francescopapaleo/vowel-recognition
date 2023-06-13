# audio-osc.py

import pyaudio
import speech_recognition as sr
import numpy as np
from pythonosc import udp_client

from formants import detect_formants


IP_ADDRESS = "127.0.0.1"
PORT = 6448
client = udp_client.SimpleUDPClient(IP_ADDRESS, PORT)

p = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
FS = 48000
CHANNELS = 1
CHUNK = 2**12
WIDTH = 2

f0min = 150
f0max = 5000

def callback(in_data, frame_count, time_info, status):
    np_buffer = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            
    formants = detect_formants(
            np_buffer, FS, CHUNK, f0min, f0max
            )
    
    print(f"Sending OSC messages to {IP_ADDRESS}:{PORT} with values: {formants}", end='\r')
    client.send_message("/wek/inputs", formants)
    
    return (in_data, pyaudio.paContinue)

stream = p.open(
    format=FORMAT,
    channels=1,
    rate=FS,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=callback
    )

stream.start_stream()

try:
    while stream.is_active():
        pass
            
except KeyboardInterrupt:
    print("Program stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()
from pythonosc import udp_client
import numpy as np
import sounddevice as sd
import time

# Initialize OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

# Initialize variables to store the latest values
latest_indata = None
latest_frames = None
latest_time = None
latest_status = None

def audio_callback(indata, frames, time, status):
    global latest_indata, latest_frames, latest_time, latest_status
    # Convert audio data to a list of floats
    audio_data = indata.flatten().tolist()

    # Send audio data over OSC
    client.send_message("/wek/inputs", audio_data)
    
    # Update the latest values
    latest_indata = indata
    latest_frames = frames
    latest_time = time
    latest_status = status

# Set up audio parameters
sample_rate = 44100
print_interval = 0.1  # Print interval in seconds (100 ms)

# Start the audio stream and capture microphone input
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Audio stream started. Press Ctrl+C to stop.")
    try:
        start_time = time.time()
        while True:
            # Check if the print interval has elapsed
            if time.time() - start_time >= print_interval:
                # print("-------------------------------")
                # # print(f"indata: {latest_indata}, frames: {latest_frames}, time: {latest_time}, status: {latest_status}")
                start_time = time.time()  # Reset the start time
    except KeyboardInterrupt:
        print("Audio stream stopped.")

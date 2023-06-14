import socket
import time
import pyaudio
import numpy as np
from threading import Thread, Event
from typing import List

from audio_features import extract_audio_features
from pythonosc import udp_client, osc_server, dispatcher as osc_dispatcher

WEK_REC_IP = "127.0.0.1"
WEK_REC_PORT = 6448

LOCALHOST_IP = "localhost"
LOCAL_VIDEO_PORT = 8338
LOCAL_AUDIO_PORT = 8339

WEK_INPUTS = "/wek/inputs"

FORMAT = pyaudio.paInt16        # 16-bit resolution
FS = 48000                      # Sampling rate
CHANNELS = 1                    # 1 channel
CHUNK = 2**12                   # 2**12 samples for buffer

# 4 audio channels for formants and 1 for loudness
audio_features = [0.0, 0.0, 0.0, 0.0, 0.0]

# 8 video channels for face features
new_message = {
    "/gesture/mouth/width": 0.0,
    "/gesture/mouth/height": 0.0,
    # "/gesture/eyebrow/left": 0.0,
    # "/gesture/eyebrow/right": 0.0,
    # "/gesture/eye/left": 0.0,
    # "/gesture/eye/right": 0.0,
    # "/gesture/jaw": 0.0,
    # "/gesture/nostrils": 0.0,
}

stop_event = Event()

def audio_processing():

    p = pyaudio.PyAudio()

    f0min = 150
    f0max = 5000
    
    global np_buffer 
    np_buffer = np.empty(CHUNK, dtype=np.int16)

    def callback(in_data, frame_count, time_info, status) -> None :
        global audio_features
        np_buffer = np.frombuffer(in_data, dtype=np.int16)
        audio_features = extract_audio_features(np_buffer, FS, CHUNK, f0min, f0max)
        return (None, pyaudio.paContinue)

    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=FS,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=0,
        stream_callback=callback
        )
    
    device_info = p.get_device_info_by_index(0)

    device_info_strs = [f"{key}: {value}" for key, value in device_info.items()]
    device_info_str = "\n".join(device_info_strs)

    stream_info_str = (
        f"\nPyAudio Stream settings:"
        f"\nSampling Frequency: {stream._rate} Hz"
        f"\nChunk Size: {stream._frames_per_buffer} samples"
        f"\nAudio Buffer Size: {stream._frames_per_buffer} samples"
        f"\nNumber of Channels: {stream._channels}"
    )
    
    print(f" \n {device_info_str}\n{stream_info_str}")

    stream.start_stream()
    print("Audio stream started. Press Ctrl+C to stop.")

    while not stop_event.is_set():
        time.sleep(1)

    stream.stop_stream()
    stream.close()
    p.terminate() 

"""
# In the OSC message handlers, update the global variable
def package_features(address, data):
global variables

features[address] = data

dispatcher = osc_dispatcher.Dispatcher()
dispatcher.map('/features', package_features)

server = osc_server.ThreadingOSCUDPServer((LOCALHOST_IP, LOCAL_AUDIO_PORT), dispatcher)
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while not stop_event.is_set():
server.handle_request()
"""

def video_processing():
    try:
        while len(new_message) > 0:
            print(f"\n Video stream started. Press Ctrl+C to stop.")
            
            # In the OSC message handlers, update the global variable
            def package_gesture(address, data):
                global new_message
                new_message[address] = data

            dispatcher = osc_dispatcher.Dispatcher()
            dispatcher.map('/gesture/mouth/width', package_gesture)
            dispatcher.map('/gesture/mouth/height', package_gesture)
            # dispatcher.map('/gesture/eyebrow/left', package_gesture)
            # dispatcher.map('/gesture/eyebrow/right', package_gesture)
            # dispatcher.map('/gesture/eye/left', package_gesture)
            # dispatcher.map('/gesture/eye/right', package_gesture)
            # dispatcher.map('/gesture/jaw', package_gesture)
            # dispatcher.map('/gesture/nostrils', package_gesture)
            
            server = osc_server.ThreadingOSCUDPServer((LOCALHOST_IP, LOCAL_VIDEO_PORT), dispatcher)
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            while not stop_event.is_set():
                server.handle_request()
    except KeyboardInterrupt:
        stop_event.set()

def main():
    global audio_features
    client = udp_client.SimpleUDPClient(WEK_REC_IP, WEK_REC_PORT)
    print(f"OSC Audio client, sending to --> {WEK_REC_IP}:{WEK_REC_PORT}")

    audio_thread = Thread(target = audio_processing)
    video_thread = Thread(target = video_processing)

    audio_thread.start()
    video_thread.start()

    try:
        while True:
            # Combine formants and video features into one list
            # /wek/inputs [f1, f2, f3, mouth_width, mouth_height]
            
            audio_features = [value for value in audio_features]
            video_features = [value for value in new_message.values()]
            message = []
            message.extend(audio_features)
            message.extend(video_features)

            client.send_message(WEK_INPUTS, message)

    except KeyboardInterrupt:
        stop_event.set()

    while audio_thread.is_alive():
        try:
            audio_thread.join(timeout=1)
        except KeyboardInterrupt:
            pass

    while video_thread.is_alive():
        try:
            video_thread.join(timeout=1)
        except KeyboardInterrupt:
            pass

    print("Program stopped.")

if __name__ == "__main__":
    main()
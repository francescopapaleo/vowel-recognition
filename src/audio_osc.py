# Audio Input -> OSC -> Wekinator

import pyaudio
import numpy as np
from pythonosc import udp_client

from audio_features import extract_audio_features

if __name__ == '__main__':
    
    SEND_TO_IP = "127.0.0.1"
    SEND_TO_PORT = 6448
    WEK_INPUT = "/wek/inputs"

    client = udp_client.SimpleUDPClient(SEND_TO_IP, SEND_TO_PORT)
    print(f"OSC Audio client, sending to --> {SEND_TO_IP}:{SEND_TO_PORT}")

    p = pyaudio.PyAudio()

    FORMAT = pyaudio.paInt16        # 16-bit resolution
    FS = 48000                      # Sampling rate
    CHANNELS = 1                    # 1 channel
    CHUNK = 2**12                   # 2**12 samples for buffer

    np_buffer = np.zeros(CHUNK, dtype=np.int16)

    f0min = 150
    f0max = 5000    

    def callback(in_data, frame_count, time_info, status) -> None :
        global np_buffer
        
        np_buffer = np.frombuffer(in_data, dtype=np.int16)
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
    
    try:
        while len(np_buffer) > 0:
            stream.start_stream()
            
            formants = extract_audio_features(np_buffer, FS, CHUNK, f0min, f0max)
            
            client.send_message(WEK_INPUT, formants)
            
            print(f"{formants}", end="\r")

    except KeyboardInterrupt:
        print("\nServer has been stopped by the user.")
        stream.stop_stream()
        stream.close()
        p.terminate()

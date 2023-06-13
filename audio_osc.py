# Audio Input -> OSC -> Wekinator

import pyaudio
import numpy as np
from pythonosc import udp_client

from formants import detect_formants

if __name__ == '__main__':

    IP_ADDRESS = "127.0.0.1"
    PORT = 6448
    WEK_INPUT = "/wek/inputs"

    client = udp_client.SimpleUDPClient(IP_ADDRESS, PORT)
    print(f"OSC client, sending to --> {IP_ADDRESS}:{PORT}")

    p = pyaudio.PyAudio()

    FORMAT = pyaudio.paInt16        # 16-bit resolution
    FS = 48000                      # Sampling rate
    CHANNELS = 1                    # 1 channel
    CHUNK = 2**12                   # 2**12 samples for buffer

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
    
    np_buffer = np.empty(CHUNK, dtype=np.int16)

    while KeyboardInterrupt != True and stream.is_active():
        stream.start_stream()
        
        # np_buffer = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        formants = detect_formants(np_buffer, FS, CHUNK, f0min, f0max)
        
        client.send_message(WEK_INPUT, formants)
        
        print(f"{formants}", end="\r")
    
    else:
        print("Program stopped.")
        stream.stop_stream()
        stream.close()
        p.terminate()
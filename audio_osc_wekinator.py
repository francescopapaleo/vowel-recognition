import sounddevice as sd
import numpy as np
from scipy.signal import filtfilt

from processing import Filter, extract_formants, butter_highpass, butter_lowpass
from pythonosc import udp_client

if __name__ == "__main__":

    sample_rate = 44100     
    block_size = 11025
    window_size = 512
    threshold = 4

    # Initialize OSC client
    client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

    def audio_callback(indata, frames, time, status):
        # volume_norm = np.linalg.norm(indata) * 10
        if status:
            print(f"Status: {status}")
    
        if any(indata):
            # Convert the incoming audio to a NumPy array
            buffer = np.squeeze(indata)
            buffer_highpass = filtfilt(*butter_highpass(100, sample_rate), buffer)
            buffer_lowpass = filtfilt(*butter_lowpass(8000, sample_rate), buffer)
        else:
            print("No input data")

        # Process the current audio frame using librosa
        f1, f2, f3 = extract_formants(buffer_lowpass, sample_rate)

        f1_filter = Filter(window_size, threshold)
        f2_filter = Filter(window_size, threshold)
        f3_filter = Filter(window_size, threshold)

        f1_filter.add_data_point(f1)
        f3_filter.add_data_point(f3)
        f2_filter.add_data_point(f2)
        
        f2 = f2_filter.calculate_average()
        f1 = f1_filter.calculate_average()
        f3 = f3_filter.calculate_average()
        
        formants = [float(f1), float(f2), float(f3)]
        client.send_message("/wek/inputs", formants)


    # Query available input devices
    input_devices = sd.query_devices()
    input_device_name = input_devices[0]["name"]  # Access the first device in the tuple and retrieve the name

    # Start the audio stream and capture microphone input
    with sd.InputStream(callback=audio_callback, 
                        channels=1, 
                        samplerate=sample_rate, 
                        device=0,
                        blocksize=block_size,
                        ):
        print(f"Selected audio device: {input_device_name}")
        print("Audio stream started. Press Ctrl+C to stop.")
        try:
            while True:
                pass  # Keeps the program running until interrupted
        except KeyboardInterrupt:
            print("Audio stream stopped.")
        except Exception as e:
            print(f"Error in audio_callback: {e}")


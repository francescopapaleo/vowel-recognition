import pyaudio
import speech_recognition as sr
import numpy as np
from threading import Thread, Event

from formants import detect_formants
from pythonosc import udp_client, osc_server, dispatcher as osc_dispatcher

# Initialize global variables for audio and video features
formants = [0.0, 0.0]
new_message = {
    "/gesture/mouth/width": 0.0,
    "/gesture/mouth/height": 0.0,
    # Add here other gestures you want to send to Wekinator
}
sample_rate = 44100     
chunk_size = 128

ip = "127.0.0.1"            # Wekinator's IP address  
receiving_from = 8338       # Port to receive messages from

stop_event = Event()  # This event will be set when the program is interrupted

def audio_processing():
    global formants
    r = sr.Recognizer()

    print("Audio stream started. Press Ctrl+C to stop.")
    try:
        with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
            while not stop_event.is_set():
                audio_data = r.record(source, duration=chunk_size / sample_rate)
                indata = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)

                if any(indata):             # and rms_dbfs > gate_threshold_dbfs:
                    buffer = indata.ravel()

                    # Add a small constant to the audio data to prevent division by zero
                    # buffer = buffer + 1e-10

                    f1_mean, f2_mean, f1_median, f2_median = detect_formants(
                        buffer, sample_rate, f0min=100, f0max=3000)
                    f1 = f1_mean
                    f2 = f2_mean
                    formants = [float(f1), float(f2)]
                else:
                    print('no input')
    except KeyboardInterrupt:
        stop_event.set()
    print("Audio stream stopped.")

def video_processing():
    print("Video stream started. Press Ctrl+C to stop.")
    
    # In the OSC message handlers, update the global variable
    def package_gesture(address, data):
        global new_message
        new_message[address] = data

    dispatcher = osc_dispatcher.Dispatcher()
    dispatcher.map('/gesture/mouth/width', package_gesture)
    dispatcher.map('/gesture/mouth/height', package_gesture)
    
    server = osc_server.ThreadingOSCUDPServer((ip, receiving_from), dispatcher)
    while not stop_event.is_set():
        server.handle_request()

def main():
    audio_thread = Thread(target=audio_processing)
    video_thread = Thread(target=video_processing)
    audio_thread.start()
    video_thread.start()

    client = udp_client.SimpleUDPClient('127.0.0.1', 6448)

    try:
        while True:
            # Combine formants and video features into one list
            # /wek/inputs [f1, f2, f3, mouth_width, mouth_height]
            message = formants + list(new_message.values())
            client.send_message("/wek/inputs", message)
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
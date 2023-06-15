import socket
from threading import Thread
from pythonosc import udp_client, osc_server, dispatcher

WEK_REC_IP = "127.0.0.1"
WEK_REC_PORT = 6448
WEK_INPUTS = "/wek/inputs"

LOCALHOST_IP = "localhost"
LOCAL_VIDEO_PORT = 8338
LOCAL_AUDIO_PORT = 8339

# 5 audio features
new_audio_msg = [0.0, 0.0, 0.0, 0.0, 0.0]

# 8 video channels for face features
new_video_msg = {
    "/gesture/mouth/width": 0.0,
    "/gesture/mouth/height": 0.0,
}

def audio_handler(unused_addr, *args):
    global new_audio_msg
    new_audio_msg = list(args)

def video_handler(addr, *args):
    global new_video_msg
    new_video_msg[addr] = args[0] if args else 0.0

def main():
    disp = dispatcher.Dispatcher()
    disp.map("/audio", audio_handler)
    disp.map("/gesture/mouth/width", video_handler)
    disp.map("/gesture/mouth/height", video_handler)

    # Audio OSC Server
    audio_server = osc_server.ThreadingOSCUDPServer((LOCALHOST_IP, LOCAL_AUDIO_PORT), disp)
    audio_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    audio_thread = Thread(target=audio_server.serve_forever)
    audio_thread.start()
    print(f"OSC Audio server, listening on --> {LOCALHOST_IP}:{LOCAL_AUDIO_PORT}")

    # Video OSC Server
    video_server = osc_server.ThreadingOSCUDPServer((LOCALHOST_IP, LOCAL_VIDEO_PORT), disp)
    video_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    video_thread = Thread(target=video_server.serve_forever)
    video_thread.start()
    print(f"OSC Video server, listening on --> {LOCALHOST_IP}:{LOCAL_VIDEO_PORT}")

    # OSC Client
    client = udp_client.SimpleUDPClient(WEK_REC_IP, WEK_REC_PORT)
    print(f"OSC Audio client, sending to --> {WEK_REC_IP}:{WEK_REC_PORT}")

    try:
        while True:
            # Combine audio and video features into one list
            audio_features = [value for value in new_audio_msg]
            video_features = [value for value in new_video_msg.values()]
            message = []
            message.extend(audio_features)
            message.extend(video_features)

            client.send_message(WEK_INPUTS, message)

    except KeyboardInterrupt:
        audio_server.shutdown()
        video_server.shutdown()
        audio_thread.join()
        video_thread.join()

    print("Program stopped.")

if __name__ == "__main__":
    main()

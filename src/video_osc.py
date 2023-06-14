# FaceOSC -> Wekinator

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

if __name__ == '__main__':

    IP_ADDRESS = "127.0.0.1"
    SENDING_TO = 6448
    RECEIVING_FROM = 8338
    WEK_INPUT = "/wek/inputs"

    client = udp_client.SimpleUDPClient(IP_ADDRESS, SENDING_TO)
    print(f"OSC Video client, sending to --> {IP_ADDRESS}:{SENDING_TO}")

    new_message = {
        "/gesture/mouth/width": 0.0,
        "/gesture/mouth/height": 0.0,
        "/gesture/eyebrow/left": 0.0,
        "/gesture/eyebrow/right": 0.0,
        "/gesture/eye/left": 0.0,
        "/gesture/eye/right": 0.0,
        "/gesture/jaw": 0.0,
        "/gesture/nostrils": 0.0,
    }

    def package_gesture(address, data):
        new_message[address] = data
        message = list(new_message.values())
        client.send_message(WEK_INPUT, message)

    def raw_handler(unused_addr, *args):
        '''we don't use raw messages but they can be handled here'''
        pass
    
    dispatcher = Dispatcher()
    
    dispatcher.map('/gesture/mouth/width', package_gesture)
    dispatcher.map('/gesture/mouth/height', package_gesture)
    dispatcher.map('/gesture/eyebrow/left', package_gesture)
    dispatcher.map('/gesture/eyebrow/right', package_gesture)
    dispatcher.map('/gesture/eye/left', package_gesture)
    dispatcher.map('/gesture/eye/right', package_gesture)
    dispatcher.map('/gesture/jaw', package_gesture)
    dispatcher.map('/gesture/nostrils', package_gesture)

    dispatcher.map("/raw", raw_handler)

    try:
        server = osc_server.ThreadingOSCUDPServer((IP_ADDRESS, RECEIVING_FROM), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer has been stopped by the user.")
        server.server_close()


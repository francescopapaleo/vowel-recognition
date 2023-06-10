'''
FaceOSC Router for Wekinator
------------------------
By default, Wekinator listens for its input messages on port 6448. The default input message is 
/wek/inputs and each input must be sent as a float within this message. This router is intended
for use with it'''

import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

new_message = {
    "/gesture/mouth/width": 0.0,
    "/gesture/mouth/height": 0.0,
    # Add here other gestures you want to send to Wekinator
}

wekinator_address = "/wek/inputs"

def package_gesture(address, data):
    print(f'{address}: {data}')
    new_message[address] = data
    message = list(new_message.values())
    print(f'Sending message to Wekinator: {message}')  # Add this line for debugging
    client.send_message(wekinator_address, message)

def raw_handler(unused_addr, *args):
    '''for now we ignore raw messages'''
    pass

if __name__ == '__main__':

    ip = "127.0.0.1"            # Wekinator's IP address
    receiving_from = 8338       # Port to receive messages from
    sending_to = 6448           # Port to send messages to

    client = udp_client.SimpleUDPClient(ip, sending_to)
    print("Sending to {} on port {}".format(ip, sending_to))
    
    dispatcher = Dispatcher()
    dispatcher.map('/gesture/mouth/width', package_gesture)
    dispatcher.map('/gesture/mouth/height', package_gesture)
    
    # Map other gestures here like the two above


    dispatcher.map("/raw", raw_handler)

    try:
        server = osc_server.ThreadingOSCUDPServer((ip, receiving_from), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer has been stopped by the user.")
        
        # Optionally add any cleanup here



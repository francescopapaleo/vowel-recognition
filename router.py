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
    ip = "127.0.0.1"
    receiving_from = 8338
    sending_to = 6448

    client = udp_client.SimpleUDPClient(ip, sending_to)
    print("Sending to {} on port {}".format(ip, sending_to))
    
    dispatcher = Dispatcher()
    dispatcher.map('/gesture/mouth/width', package_gesture)
    dispatcher.map('/gesture/mouth/height', package_gesture)
    # Map other gestures here like the two above

    dispatcher.map("/raw", raw_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, receiving_from), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

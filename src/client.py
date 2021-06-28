import socket
from time import sleep, ctime
import threading
import json
from colorama import init, Fore, Style
import random

"""
Colorama's Constant
"""
init()
COLORS = [Fore.RED, Fore.GREEN, Fore.CYAN, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.LIGHTRED_EX
          ]

USER_THEME_COLOR = random.choice(COLORS)
TEXT_COLOR = Fore.BLUE


HEADER = 64
PORT = 6969

FORMAT = 'utf-8'
SERVER = "192.168.56.1"  # Enter the IP address of your machine

NICKNAME = []

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)


def reconnect():  # To reconnect the server, if the connection is lost
    connected = False
    global client  # To make sure client-socket which is connected with server is same for send as well as receive function..
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connection lost, Reconnecting!..")
    while not connected:
        try:
            client.connect(ADDR)
            client.send(NICKNAME[0].encode(FORMAT))
            connected = True
            print("Connection Re-established")
            return
        except socket.error:
            sleep(3)


def receive_message():
    while True:
        try:
            recv_msg_length = client.recv(HEADER).decode(FORMAT)
            if recv_msg_length:
                recv_message = json.loads(client.recv(int(recv_msg_length)).decode(FORMAT))
                print(f"[{TEXT_COLOR+Style.DIM+ctime()}]:: {recv_message['USER_THEME_COLOR']+Style.BRIGHT+recv_message['sender']}:-"
                      f"  {TEXT_COLOR+Style.BRIGHT+recv_message['msg']}")
            else:
                return False
        except ConnectionError:
            reconnect()
            continue



thread = threading.Thread(target=receive_message, daemon=True)
thread.start()


def send(msg):
    message = json.dumps({'sender': NICKNAME[0], 'msg':msg, 'USER_THEME_COLOR':USER_THEME_COLOR})  # It'll encode the string in byte like object
    msg_length = len(str(message))
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    try:
        client.send(send_length)
        client.sendall(bytes(message, FORMAT))
        return True
    except ConnectionError:
        return False


nickname_ = input(TEXT_COLOR+Style.BRIGHT+"Enter the nickname:- ")
nickname_ = '@' + nickname_
client.send(nickname_.encode(FORMAT))
NICKNAME.append(nickname_)

print(TEXT_COLOR+Style.BRIGHT+"Type the message and hit Enter")
while True:
    msg_ = input()
    if len(msg_) > 0 and set(msg_) != {' '}:
        success = send(msg_)
        if not success:
            reconnect()
    else:
        print(TEXT_COLOR+Style.BRIGHT+"Enter the Valid Message")

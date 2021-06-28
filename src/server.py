import socket
import threading

userdata = {}  # To store the username and client-Address
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
HEADER = 64  # It is nothing but buffer size

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_IP, PORT))


def handle_client(client_socket):
    nickname = userdata[client_socket]
    print(f"{nickname} is connected!..")
    while True:
        try:
            msg_length = client_socket.recv(HEADER).decode('utf-8')
            if msg_length:
                message = client_socket.recv(int(msg_length))
                msg_length = msg_length.encode('utf-8')
                msg_length += b' ' * (HEADER - len(msg_length))
                for i in userdata:
                    i.send(msg_length)
                    i.send(message)
            else:
                return False
        except ConnectionResetError:
            print(f"{nickname} has left the chat")
            del userdata[client_socket]
            break

    client_socket.close()


def start():
    server.listen(20)
    print(f"Server is listening on {SERVER_IP:{PORT}}")
    while True:
        try:
            client_socket, addr = server.accept()
            userdata[client_socket] = client_socket.recv(HEADER).decode('utf-8')
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            print(f"No of active connections are {threading.activeCount()-1}")

        except ConnectionError:
            pass


print("Server is Starting")
start()
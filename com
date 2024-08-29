import socket
import threading
from enum import Enum

HOST = "127.0.0.1"
PORT = 5555
MAX_BYTE = 1024

client_socket = None


def send_message(data):
    try:
        client_socket.send(data.encode())
    except Exception as e:
        print(f"Error: {e}")


def server(host, port):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected")

    try:
        user_input = int(input("Please enter 1 to move, 2 to stop: "))
        message = MessageType(user_input)
    except ValueError:
        print("Please enter a valid number.")
        return

    receive_thread = threading.Thread(target=listener, args=(client_socket,))
    receive_thread.start()
    
    send_message(str(user_input))


def listener(client_socket):
    while True:
        try:
            data = client_socket.recv(MAX_BYTE)
            if data:
                print(MessageType(int(data.decode())))
            else:
                break
        except:
            print("\nConnection lost.")
            break


class MessageType(Enum):
    move = 1
    stop = 2


server(HOST, PORT)

import socket
import threading
import time
from enum import Enum
from turtledemo.clock import datum
from xml.sax.saxutils import escape

from httpcore import SOCKET_OPTION

HOST = "127.0.0.1"
PORT = 5555
CLIENT_ID = 2
MAX_BYTE = 1024

client_socket = None


def send_message(Data):
    try:
        client_socket.send(Data.to_bytes())
    except Exception as  e:
        print(f"Hata {e}")


def server(host,port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected")
    try:
        user_input = int(input("Plese enter 1 for start 2 for stop"))
        message = MessageType(user_input)
    except:
        print("PLese enter a number")
    receive_thread = threading.Thread(target=listener(client_socket), args=(client_socket,))
    receive_thread.start()
    send_message(user_input)


def listener(client_socket):
    while True:
        try:
            data = client_socket.recv(MAX_BYTE)
            if data:
                print(MessageType(data.decode()))
            else:
                break
        except:
            print("\nBağlantı koptu.")
            break


class MessageType(Enum):
    move = 1
    stop = 2



server(HOST,PORT)

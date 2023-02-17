import socket
import threading


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.47"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)   # encodes string into a bytes like object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   # adds 0's untill filling the 64 bytes
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))     # just a big number bc lazy, ideally we should do as in the other way
    # if we wanted to send objects instead of strings, we can use "JASON" or "PICKLE"


send("Hello world!")
input()
send("HOLAHOLAHOLAHOLA")
input()
send(DISCONNECT_MESSAGE)

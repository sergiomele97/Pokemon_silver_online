import socket
import threading
import pickle

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# we are using private ip address (local network only), if we want it public we should put our public IP
server.bind(ADDR)


class player:
    def __init__(self, px, py, px_correction, py_correction, pnumber):
        self.px = px
        self.py = py
        self.px_correction = px_correction
        self.py_correction = py_correction
        self.pnumber = pnumber


player_list = []
player_list.append(player(0, 0, 0, 0, 0))
address_player_dict = {}


def handle_client(conn, addr):
    print(f"[NEW CONNECTION {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)   # how many bytes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # We get the message and actualize server's info
            player_data = msg.split(sep=",")   # splitting message into 4 variables (Incoming format ex: "8,7,5,5")
            player_list[address_player_dict[addr]].px = (int(player_data[0]))
            player_list[address_player_dict[addr]].py = (int(player_data[1]))
            player_list[address_player_dict[addr]].px_correction = (int(player_data[2]))
            player_list[address_player_dict[addr]].py_correction = (int(player_data[3]))

            print(f"[{addr}] {msg}")

            # We send back all the info // Pickle makes object --> string transition easier
            # Send their player number on the player_list[0].pnumber
            player_list[0].pnumber = player_list[address_player_dict[addr]].pnumber
            output_message = pickle.dumps(player_list)
            conn.send(output_message)   # We send the object with the players

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    player_counter = 0

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        player_counter += 1  # We increase player number by 1
        player_list.append(player(0, 0, 0, 0, player_counter))    # We add a new object player to the list
        address_player_dict[addr] = player_counter    # We link each address to its object player


        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    pass


print("[STARTING] server is starting...")
start()

from pyboy import PyBoy, WindowEvent
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
import socket
import pickle

# Creates an emulator instance and charges the saved emulator state
pyboy = PyBoy("C:/Users/Sergio/PycharmProjects/Pyboy/Pokemon_Silver.gbc")
file_like_object = open("state_file.state", "rb")
pyboy.load_state(file_like_object)
pyboy.set_emulation_speed(4)


# Declares window, title and dimensions
window = Tk()
window.title("Pokemon silver online")
window.geometry("480x432")  # 10x9 possible positions on screen


# Initializes the label which contains the images
array = pyboy.botsupport_manager().screen().screen_ndarray()
img = ImageTk.PhotoImage(image=Image.fromarray(array))
panel = Label(window, image=img)
panel.pack(side="bottom", fill="both", expand="true")


# Sprite stuff
sprite = Image.open("sprite2.png")
npsprite = np.asarray(sprite)
npsprite = npsprite.repeat(3, axis=0).repeat(3, axis=1)
x_correction = 0
y_correction = 0
last_sprite_x = 0
last_sprite_x2 = 0
last_sprite_x3 = 0      # In order to be fluid, we need information from 3 ticks before.
last_sprite_y = 0
last_sprite_y2 = 0
last_sprite_y3 = 0
last_self_x = 0
last_self_y = 0
set_sprite_x = 0
set_sprite_y = 0


# borders to avoid crashes
x_border = np.zeros([48, 480, 3])
y_border = np.zeros([48, 528, 3])


# CLIENT SETUP
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.47"
ADDR = (SERVER, PORT)
player_number = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# END OF CLIENT SETUP


class player:
    def __init__(self, px, py, px_correction, py_correction, pnumber):
        self.px = px
        self.py = py
        self.px_correction = px_correction
        self.py_correction = py_correction
        self.pnumber = pnumber


def send(msg):
    message = msg.encode(FORMAT)   # encodes string into a bytes like object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   # adds 0's untill filling the 64 bytes
    client.send(send_length)
    client.send(message)

    output_message = client.recv(24000)   # just a big number bc lazy, ideally we should do as in the other way
    play_list = pickle.loads(output_message)

    return play_list  # The function returns the list of players


# Emulator's main loop which actualizes the online window
while not pyboy.tick():

    # Gets RAM memory information related to character location
    self_x = pyboy.get_memory_value(55811)
    self_y = pyboy.get_memory_value(55810)
    sprite_x = pyboy.get_memory_value(53780)    # 16 points every step on map, actualizes 8 times per step
    sprite_y = pyboy.get_memory_value(53781)

    if pyboy.get_input():
        print("X=" + str(self_x) + " Y=" + str(self_y))

    # Get the new frame
    array = pyboy.botsupport_manager().screen().screen_ndarray()

    # Resizing array
    big_array = array.repeat(3, axis=0).repeat(3, axis=1)   # Increases pixel number
    big_array = np.insert(big_array, 0, x_border, 0)
    big_array = np.insert(big_array, big_array.shape[0], x_border, 0)
    big_array = np.insert(big_array, 0, y_border, 1)
    big_array = np.insert(big_array, big_array.shape[0], y_border, 1)

    # Printing online info into de array

    arraycopy = np.array(big_array, copy=TRUE)       # FOR SOME REASON THIS IS NECESSARY FOR COPYING NP.ARRAYS!

    if last_self_x != self_x:
        set_sprite_x = sprite_x
    if last_self_y != self_y:
        set_sprite_y = sprite_y

    # Correction for sprite_x and sprite_y reset to 64 after event
    if sprite_x == 64 and sprite_y == 64 and abs(last_sprite_x - sprite_x) + abs(last_sprite_y - sprite_y) > 10:
        last_sprite_x = 64
        last_sprite_x2 = 64
        last_sprite_x3 = 64
        set_sprite_x = 64
        last_sprite_y = 64
        last_sprite_y2 = 64
        last_sprite_y3 = 64
        set_sprite_y = 64
    # End of correction

    # Correction for passing x and y borders
    if last_sprite_x == 0 and sprite_x == 254:  # Moving past left border
        last_sprite_x = 256
        last_sprite_x2 = 256
        last_sprite_x3 = 256
        set_sprite_x = 256
    if last_sprite_y == 0 and sprite_y == 254:  # Moving past top border
        last_sprite_y = 256
        last_sprite_y2 = 256
        last_sprite_y3 = 256
        set_sprite_y = 256
    # End of correction

    x_correction = last_sprite_x3 - set_sprite_x
    y_correction = last_sprite_y3 - set_sprite_y

    # Sending position to the server and receiving the player_list
    player_list = send(str(self_x) + "," + str(self_y) + "," + str(x_correction) + "," + str(y_correction) + "," + str(player_number))
    player_number = player_list[0].pnumber

    players_insight = []

    # Printing players
    for Online_player in player_list:       # Never reuse variable names
        x = (Online_player.px + 5 - self_x) * 48 - (x_correction - Online_player.px_correction) * 3
        y = (Online_player.py + 5 - self_y) * 48 - (y_correction - Online_player.py_correction) * 3 - 12

        if (0 < x < 11*48) and (0 < y < 10*48) and player_number != Online_player.pnumber:  # Esto va lento
            big_array[y:y + npsprite.shape[0], x:x + npsprite.shape[1]] = npsprite

            arraycopy = np.where(big_array == 255, arraycopy, big_array)
    # End of printing players


    '''
    if pyboy.get_input():
        print("x=" + str(x) + " y=" + str(y))
        print("sprite_x=" + str(sprite_x) + " sprite_y=" + str(sprite_y))
    '''
    # Correction for passing x and y borders
    if last_sprite_x2 == 252 and last_sprite_x == 254 and sprite_x == 254:    # Next tick sprite_x will be 0
        last_sprite_x = - 2
        last_sprite_x2 = - 2
        last_sprite_x3 = - 4
    else:
        last_sprite_x3 = last_sprite_x2
        last_sprite_x2 = last_sprite_x
        last_sprite_x = sprite_x

    if last_sprite_y2 == 252 and last_sprite_y == 254 and sprite_y == 254:    # Next tick sprite_y will be 0
        last_sprite_y = - 2
        last_sprite_y2 = - 2
        last_sprite_y3 = - 4
    else:
        last_sprite_y3 = last_sprite_y2
        last_sprite_y2 = last_sprite_y
        last_sprite_y = sprite_y
    # End of correction

    last_self_x = self_x
    last_self_y = self_y

    # Updating label with the img
    img = ImageTk.PhotoImage(image=Image.fromarray(arraycopy))
    panel.configure(image=img, height=440, width=480)
    window.update_idletasks()
    window.update()

    pass

'''
print(np.shape(big_array))
print(np.shape(npsprite))
'''

# Saves emulator state into a file
file_like_object = open("state_file.state", "wb")
pyboy.save_state(file_like_object)

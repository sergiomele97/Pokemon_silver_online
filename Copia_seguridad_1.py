from pyboy import PyBoy, WindowEvent
from tkinter import *
import numpy as np
from PIL import ImageTk, Image


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


sprite = Image.open("sprite1.png")
npsprite = np.asarray(sprite)
# npsprite = npsprite.repeat(3, axis=0).repeat(3, axis=1)


# Emulator's main loop which actualizes the online window
while not pyboy.tick():

    # Gets RAM memory information related to character location
    if pyboy.get_input():
        print("X=" + str(pyboy.get_memory_value(55811)) + " Y=" + str(pyboy.get_memory_value(55810)))

    # Get the new frame and
    array = pyboy.botsupport_manager().screen().screen_ndarray()
    # Printing online info into de array
    array = np.where(npsprite != 255, npsprite, array)
    # Resizing array
    big_array = array.repeat(3, axis=0).repeat(3, axis=1)   # Increases pixel number


    # Updating label with the img
    img = ImageTk.PhotoImage(image=Image.fromarray(big_array))
    panel.configure(image=img, height=440, width=480)
    window.update_idletasks()
    window.update()

    pass


print(np.shape(big_array))
print(np.shape(npsprite))


# Saves emulator state into a file
file_like_object = open("state_file.state", "wb")
pyboy.save_state(file_like_object)

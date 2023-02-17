from pyboy import PyBoy


pyboy = PyBoy("C:/Users/Sergio/PycharmProjects/Pyboy/Pokemon_Silver.gbc")
pyboy.set_emulation_speed(4)
file_like_object = open("state_file.state", "rb")
pyboy.load_state(file_like_object)


while not pyboy.tick():
    pass


# Saves emulator state into a file
file_like_object = open("state_file.state", "wb")
pyboy.save_state(file_like_object)

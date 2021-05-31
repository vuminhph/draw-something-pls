# import all the required modules
from tkinter import *
# from PIL import Image

import time
from _thread import *

from classes.windows.LoginWindow import LoginWindow
from classes.windows.WaitingWindow import WaitingWindow
from classes.windows.GuesserWindow import GuesserWindow
from classes.GameController import GameController
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role
from classes.Timer import Duration

# import threading
# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, host: str, port: int):
        self.__game_controller = GameController(host, port)

        # chat window which is currently hidden
        self.__game_window = Tk()
        self.__game_window.withdraw()

        self.display_login_window()

    def get_game_controller(self):
        return self.__game_controller

    def get_game_window(self):
        return self.__game_window

    def set_username(self, username: str):
        self.__username = username

    def display_login_window(self):
        login_window = LoginWindow(self)
        login_window.set_GUI(self)

    def display_waiting_window(self):
        waiting_window = WaitingWindow(self)
        waiting_window.set_GUI(self)

    def display_game_window(self, reply_msg):
        # print the player's role
        if reply_msg['role'] == Role.Drawer:
            print('You have been assigned the role of Drawer')
            # Create the drawing window
            # TODO
        elif reply_msg['role'] == Role.Guesser:
            print('You have been assigned the role of Guesser')
            # Create the guessing window
            # TODO

    def display_guesser_window(self, username):
        pass

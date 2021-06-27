# import all the required modules
from classes.windows.LoginWindow import LoginWindow
from classes.windows.WaitingWindow import WaitingWindow
from classes.windows.GuesserWindow import GuesserWindow
from classes.GameController import GameController
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role
from classes.Timer import Duration
from classes.windows.FirstWindow import FirstWindow

import Paint.paint  # For demo

from tkinter import *
# from PIL import Image
import time
# import threading
from _thread import *


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
        # LoginWindow(self)
        FirstWindow(self)

    def display_waiting_window(self):
        WaitingWindow(self)

    def display_game_window(self, reply_msg):

        if reply_msg['role'] == Role.Drawer:
            print('You have been assigned the role of Drawer')
            self.__display_drawer_window()

        elif reply_msg['role'] == Role.Guesser:
            players = reply_msg['players_dict']
            print('You have been assigned the role of Guesser')
            self.__display_guesser_window(self.__username, players)

    def __display_guesser_window(self, username, players):
        GuesserWindow(self, username, players)

    def __display_drawer_window(self):
        Paint()

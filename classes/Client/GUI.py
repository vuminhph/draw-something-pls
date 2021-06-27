# import all the required modules
from classes.Client.windows.LoginWindow import LoginWindow
from classes.Client.windows.WaitingWindow import WaitingWindow
from classes.Client.windows.GuesserWindow import GuesserWindow
from classes.Client.windows.PaintWindow import PaintWindow
from classes.Client.GameController import GameController

from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role


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

    def get_username(self):
        return self.__username

    def set_username(self, username: str):
        self.__username = username

    def display_login_window(self):
        LoginWindow(self)

    def display_waiting_window(self):
        WaitingWindow(self)

    def display_game_window(self, reply_msg):
        if reply_msg['role'] == Role.Drawer:
            print('You have been assigned the role of Drawer')
            keyword = reply_msg['keyword']
            self.__display_drawer_window(keyword)

        elif reply_msg['role'] == Role.Guesser:
            print('You have been assigned the role of Guesser')
            players = reply_msg['players_dict']
            drawer_name = reply_msg['drawer_name']
            obc_keyword = reply_msg['obc_keyword']

            self.__display_guesser_window(
                self.__username, players, drawer_name, obc_keyword)
        self.__game_controller.reset_round()

    def __display_guesser_window(self, username, players, drawer_name, obc_keyword):
        window = GuesserWindow(self, username, players,
                               drawer_name, obc_keyword)
        window.start_mainloop()

    def display_guesser_window_from_drawer(self, players, drawer_name):
        window = GuesserWindow(self, self.__username,
                               players, drawer_name, is_drawer=True)
        window.from_drawer_init()
        window.start_mainloop()

    def __display_drawer_window(self, keyword):
        PaintWindow(self, keyword)

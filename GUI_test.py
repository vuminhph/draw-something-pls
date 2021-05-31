# from classes.GameController import GameController
# from classes.enums.ApplicationCode import ApplicationCode
# from classes.enums.Role import Role
# from classes.Timer import Duration

# import all the required modules
from os import stat
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext
# from PIL import Image

import time
from _thread import *
import tkinter

# import threading
# GUI class for the chat


class GameWindow:
    # constructor method
    def __init__(self):
        # self.__game_controller = GameController(host, port)

        # chat window which is currently hidden
        self.__game_window = Tk()
        # self.__game_window.withdraw()

        # login_window = LoginWindow(self.__game_controller)
        # login_window.set_GUI(self)
        # self.__game_window.mainloop()

    def set_username(self, username: str):
        self.__username = username

    # def display_waiting_window(self):
    #     waiting_window = WaitingWindow(self.__game_controller)
    #     waiting_window.set_GUI(self)

    def display_game_window(self):
        # Game window
        self.__game_window.deiconify()
        self.__game_window.title("GAME ROOM #1")
        self.__game_window.resizable(width=False,
                                     height=False)
        self.__game_window.configure(width=1280,
                                     height=720)

        # Player name
        self.__playerName = Label(self.__game_window,
                                  font=("Arial", 20),
                                  text='Player: '+self.__username,
                                  fg="red",
                                  bg="white",
                                  relief="ridge")
        self.__playerName.place(relheight=0.08,
                                relwidth=0.23,
                                relx=0.01,
                                rely=0.01)

        # Message title
        self.__msg_title = StringVar()
        self.__msg_title.set("Message")

        self.__msg_label = Label(self.__game_window,
                                 textvariable=self.__msg_title,
                                 font=("Times New Roman", 20, "italic"),
                                 fg="green",
                                 bg="white",
                                 relief="ridge")
        self.__msg_label.place(relheight=0.08,
                               relwidth=0.45,
                               relx=0.25,
                               rely=0.01)
        
        # Timer
        self.__timer = StringVar()
        self.__timer.set("60")

        self.__timer_label = Label(self.__game_window,
                                   textvariable=self.__timer,
                                   font=("Consolas", 35, "bold"),
                                   fg="blue",
                                   bg="white",
                                   relief="ridge")
        self.__timer_label.place(relheight=0.08,
                               relwidth=0.28,
                               relx=0.71,
                               rely=0.01)

        # Scoreboard
        self.__scoreboard__label = Label(self.__game_window,
                                        text="Scoreboard",
                                        font=("Arial", 14),
                                        bg="black",
                                        fg="white")
        self.__scoreboard__label.place(relheight=0.05,
                                       relwidth=0.23,
                                       relx=0.01,
                                       rely=0.1)
                                      
        # self.__scoreboard_list = StringVar()
        # self.__scoreboard_list.set("Table")

        self.__scoreboard__table = Text(self.__game_window,
                                        font="Arial 14",
                                        relief="solid",
                                        state=DISABLED,
                                        cursor="arrow")
        self.__scoreboard__table.place(relheight=0.75,
                                       relwidth=0.23,
                                       relx=0.01,
                                       rely=0.15)

        # Picture room
        pictName = './images/@NVH-play.png'  # Define picture pathname
        self.__pict = PhotoImage(file=pictName)
        self.__pictureRoom = Label(self.__game_window,
                                   image=self.__pict,
                                   borderwidth=2,
                                   relief="ridge",
								   bg="white")
        self.__pictureRoom.place(relheight=0.8,
                                 relwidth=0.45,
                                 relx=0.25,
                                 rely=0.1)

        # Chat room
        self.__chatRoom = scrolledtext.ScrolledText(self.__game_window,
                                                    width=20,
                                                    height=2,
                                                    bg="#17202A",
                                                    fg="white",
                                                    font="Arial 14",
                                                    cursor="arrow",
                                                    state=DISABLED,
                                                    padx=2,
                                                    pady=5)
        self.__chatRoom.place(relheight=0.8,
                              relwidth=0.28,
                              relx=0.71,
                              rely=0.1)

        # Answering place
        self.__answer_label = Label(self.__game_window,
                                    text="Your answer:",
                                    font="Arial 14 bold",
									anchor=E)
        self.__answer_label.place(relheight=0.06,
								  relwidth=0.23,
								  relx=0.01,
                                  rely=0.92)

        self.__answer_entry = Entry(self.__game_window,
                                bg="#2C3E50",
                                fg="#EAECEE",
                                font="Arial 14")
        self.__answer_entry.place(relheight=0.06,
                              relwidth=0.45,
                              relx=0.25,
                              rely=0.92)
        self.__answer_entry.focus()

        self.__answer_send = Button(self.__game_window,
                                    text="Send",
                                    font="Arial 12 bold",
                                    width=20,
                                    bg="#ABB2B9",
                                    command=lambda: self.__send_answer(self.__answer_entry.get()))
        self.__answer_send.place(relheight=0.06,
                               relwidth=0.07,
                               relx=0.71,
                               rely=0.92)
        
        # Test showing the window
        self.__game_window.mainloop()

    def __send_answer(self, msg):
        self.__chatRoom.configure(state=NORMAL)
        self.__display_answer('Hoang', msg)
        self.__answer_entry.delete(0, END)
        self.__chatRoom.configure(state=DISABLED)

    def __display_answer(self, username, answer):
        self.__chatRoom.insert(END, username + ': ' + answer + '\n\n')
        self.__chatRoom.see(END)
    
    def __display_leaderboard(self, scoreboard:list):
        self.__scoreboard__table.configure(state=NORMAL)
        self.__scoreboard__table.delete(0, END)
        # Insert from scoreboard list
        # TODO
        self.__scoreboard__table.configure(state=DISABLED)

    def __reset_round(self):
        # Clear all answers of previous rounds
        self.__chatRoom.delete(0, END)

        # Update the scoreboard
        self.__display_leaderboard()

    def __wait_for_drawing(self):
        # Disable the Send button in the time of drawing
        self.__answer_send.config(state=DISABLED)


gui = GameWindow()
gui.set_username('Hoang')
gui.display_game_window()

# import all the required modules
from classes.Client.windows.DisplayWindow import DisplayWindow
import classes.Client.GUI
from classes.enums.SystemConst import SystemConst

from os import stat
from tkinter import *
from tkinter import font, ttk, scrolledtext
# from PIL import Image

import os
import time
from _thread import *
import tkinter

# import threading
# GUI class for the chat


class GuesserWindow(DisplayWindow):
    # constructor method
    def __init__(self, GUI, username: str, player_dict: dict):
        super().__init__(GUI)

        # Game window
        self._window.deiconify()
        self._window.title("GAME ROOM #1")
        self._window.resizable(width=False,
                               height=False)
        self._window.configure(width=1280,
                               height=720)

        # Player name
        self.__playerName = Label(self._window,
                                  font=("Consolas", 20),
                                  text='Player: ' + username,
                                  bg="white",
                                  relief="ridge")
        self.__playerName.place(relheight=0.08,
                                relwidth=0.23,
                                relx=0.01,
                                rely=0.01)

        # Message title
        self.__keyword_label = StringVar()
        self.__display_header("Drawing in progress...")

        self.__msg_label = Label(self._window,
                                 textvariable=self.__keyword_label,
                                 font=("Consolas", 20, "italic"),
                                 bg="white",
                                 relief="ridge")
        self.__msg_label.place(relheight=0.08,
                               relwidth=0.45,
                               relx=0.25,
                               rely=0.01)

        # Timer
        self.__clock = SystemConst.GUESSING_TIME
        self.__timer = StringVar()
        self.__timer.set(str(self.__clock))

        self.__timer_label = Label(self._window,
                                   textvariable=self.__timer,
                                   font=("Consolas", 35, "bold"),
                                   bg="white",
                                   relief="ridge")
        self.__timer_label.place(relheight=0.08,
                                 relwidth=0.28,
                                 relx=0.71,
                                 rely=0.01)

        # Scoreboard
        self.__scoreboard__label = Label(self._window,
                                         text="Scoreboard",
                                         font=("Consolas", 16, "bold"),
                                         bg="black",
                                         fg="white")
        self.__scoreboard__label.place(relheight=0.05,
                                       relwidth=0.23,
                                       relx=0.01,
                                       rely=0.1)

        self.__scoreboard__table = Text(self._window,
                                        font="Consolas 14",
                                        relief="solid",
                                        state=DISABLED,
                                        cursor="arrow",
                                        padx=5,
                                        pady=5)
        self.__scoreboard__table.place(relheight=0.75,
                                       relwidth=0.23,
                                       relx=0.01,
                                       rely=0.15)

        # Chat room
        self.__chatRoom = scrolledtext.ScrolledText(self._window,
                                                    width=20,
                                                    height=2,
                                                    bg="#17202A",
                                                    fg="white",
                                                    font="Consolas 14",
                                                    cursor="arrow",
                                                    state=DISABLED,
                                                    padx=2,
                                                    pady=5)
        self.__chatRoom.place(relheight=0.8,
                              relwidth=0.28,
                              relx=0.71,
                              rely=0.1)

        # Answering place
        self.__answer_label = Label(self._window,
                                    text="Your answer:",
                                    font="Consolas 14 bold",
                                    anchor=E)
        self.__answer_label.place(relheight=0.06,
                                  relwidth=0.23,
                                  relx=0.01,
                                  rely=0.92)

        self.__answer_entry = Entry(self._window,
                                    bg="#2C3E50",
                                    fg="#EAECEE",
                                    font="Consolas 14")
        self.__answer_entry.place(relheight=0.06,
                                  relwidth=0.45,
                                  relx=0.25,
                                  rely=0.92)
        self.__answer_entry.focus()

        self.__answer_send = Button(self._window,
                                    text="Send",
                                    font="Consolas 12 bold",
                                    width=20,
                                    bg="#ABB2B9",
                                    command=lambda: self.__send_answer(self.__answer_entry.get()))
        self.__answer_send.place(relheight=0.06,
                                 relwidth=0.07,
                                 relx=0.71,
                                 rely=0.92)

        self.__display_scoreboard(player_dict)
        # Press Enter to send answer
        self._window.bind('<Return>', lambda e: self.__send_answer(
            self.__answer_entry.get()))

        start_new_thread(self.__wait_for_drawing, ())
        self._window.mainloop()

    def __display_header(self, keyword: str):
        self.__keyword_label.set(keyword)

    def __send_answer(self, message):
        self.__display_answer(self._GUI.get_username(), message)
        self.__answer_entry.delete(0, END)
        self._game_controller.send_answer(self._GUI.get_username(), message)

    def __display_scoreboard(self, players_dict: dict):
        self.__scoreboard__table.configure(state=NORMAL)
        self.__scoreboard__table.delete(0.0, END)

        # Insert from players dictionary
        for user in players_dict.keys():
            score = players_dict[user]
            self.__scoreboard__table.insert(END, user + ': ' + score + '\n\n')

        self.__scoreboard__table.configure(state=DISABLED)

    def __reset_round(self):
        # Clear all answers of previous rounds
        self.__chatRoom.configure(state=NORMAL)
        self.__chatRoom.delete(0.0, END)
        self.__chatRoom.configure(state=DISABLED)

        # Update the scoreboard
        # self.__display_scoreboard()

    def __disable_answer(self):
        self.__answer_entry.configure(state=DISABLED)
        self.__answer_send.configure(state=DISABLED)

    def __enable_answer(self):
        self.__answer_entry.configure(state=NORMAL)
        self.__answer_send.configure(state=NORMAL)

    def __display_answer(self, username, answer):
        self.__chatRoom.configure(state=NORMAL)
        self.__chatRoom.insert(END, username + ': ' + answer + '\n\n')
        self.__chatRoom.configure(state=DISABLED)
        self.__chatRoom.see(END)

    def __wait_for_drawing(self):
        # Block input from player while waiting to receive image
        self.__disable_answer()
        if self._game_controller.receive_image(self._GUI.get_username()):
            self.__start_guessing()

    def __start_guessing(self):
        cur_dir = os.getcwd()
        save_dir = './Paint/saves/receive/'
        filename = 'image' + '_' + self._GUI.get_username() + '.png'
        image_path = os.path.join(cur_dir, save_dir, filename)

        self.__display_image(image_path)
        self.__enable_answer()
        self.__display_header("Take a guess")

        self.__count_down()
        start_new_thread(self.__listen_for_other_players_answ, ())

    def __display_image(self, filepath: str):
        self.__pict = PhotoImage(file=filepath)
        self.__pictureRoom = Label(self._window,
                                   image=self.__pict,
                                   borderwidth=2,
                                   relief="ridge",
                                   bg="white")
        self.__pictureRoom.place(relheight=0.8,
                                 relwidth=0.45,
                                 relx=0.25,
                                 rely=0.1)

    def __count_down(self):
        timer_text = str(int(round(self.__clock, 0)))
        self.__timer.set(timer_text)
        self.__clock -= 1

        if self.__clock > 0:
            self._window.after(1000, self.__count_down)
        else:
            pass
            # TODO: Send guessing timeout request

    def __listen_for_other_players_answ(self):
        reply_msg = self._game_controller.receive_answer()
        self.__display_answer(reply_msg['username'], reply_msg['message'])

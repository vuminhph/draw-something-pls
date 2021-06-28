# import all the required modules
from classes.Client.windows.DisplayWindow import DisplayWindow
import classes.Client.GUI
from classes.enums.SystemConst import SystemConst
from classes.enums.Role import Role
from classes.enums.ApplicationCode import ApplicationCode

from tkinter import *
from tkinter import font, ttk, scrolledtext

import os
import time
from _thread import *
from random import randint


class GuesserWindow(DisplayWindow):
    # constructor method
    def __init__(self, GUI, username: str, players_dict: dict, drawer_name: str, obc_keyword: str = None, is_drawer: bool = False):
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
                                  text=username,
                                  bg="white",
                                  relief="ridge")
        self.__playerName.place(relheight=0.08,
                                relwidth=0.23,
                                relx=0.01,
                                rely=0.01)

        # Message title
        self.__keyword_label = StringVar()
        self.__drawer_name = drawer_name
        self.__display_header(drawer_name + " is drawing...")

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
                                    command=lambda: self.__send_message(self.__answer_entry.get()))
        self.__answer_send.place(relheight=0.06,
                                 relwidth=0.07,
                                 relx=0.71,
                                 rely=0.92)

        self.__display_scoreboard(players_dict, drawer_name)
        # Press Enter to send answer
        self._window.bind('<Return>', lambda e: self.__send_message(
            self.__answer_entry.get()))

        self.__obc_keyword = obc_keyword
        self.__is_drawer = is_drawer
        self.__counting_down = True  # TODO: Reset every round

        start_new_thread(self.__guesser_listen, ())
        # self._window.mainloop()

    def start_mainloop(self):
        self._window.mainloop()

    def __display_header(self, header: str):
        self.__keyword_label.set(header)

    def __send_message(self, message):
        self.__display_user_message(self._GUI.get_username(), message)
        self.__answer_entry.delete(0, END)
        self._game_controller.send_message(
            self._GUI.get_username(), message, self.__clock)

    def __display_scoreboard(self, players_dict: dict, drawer_name: str):
        self.__scoreboard__table.configure(state=NORMAL)
        self.__scoreboard__table.delete(0.0, END)

        # Insert from players dictionary
        for username in players_dict.keys():
            score = players_dict[username]
            if username == drawer_name:
                self.__scoreboard__table.insert(
                    END, username + ' (drawer): ' + score + '\n\n')
            else:
                self.__scoreboard__table.insert(
                    END, username + ': ' + score + '\n\n')

        self.__scoreboard__table.configure(state=DISABLED)

    def __reset_round(self):
        # Clear all answers of previous rounds
        self.__chatRoom.configure(state=NORMAL)
        self.__chatRoom.delete(0.0, END)
        self.__chatRoom.configure(state=DISABLED)

        # Update the scoreboard
        # self.__display_scoreboard()

    def __disable_answering(self):
        self.__answer_entry.configure(state=DISABLED)
        self.__answer_send.configure(state=DISABLED)

    def __enable_answering(self):
        self.__answer_entry.configure(state=NORMAL)
        self.__answer_send.configure(state=NORMAL)

    def __display_user_message(self, username, message):
        self.__chatRoom.configure(state=NORMAL)
        self.__chatRoom.insert(END, username + ': ' + message + '\n\n')
        self.__chatRoom.configure(state=DISABLED)
        self.__chatRoom.see(END)

    def __display_game_message(self, message):
        self.__chatRoom.configure(state=NORMAL)
        self.__chatRoom.insert(END, message + '\n\n', "game_message")
        self.__chatRoom.tag_configure(
            "game_message", font=("Consolas", "14", "italic"))
        self.__chatRoom.tag_configure("game_message", foreground="yellow")
        self.__chatRoom.configure(state=DISABLED)
        self.__chatRoom.see(END)

    def __guesser_listen(self):
        # Block input from player while waiting to receive image
        self.__disable_answering()
        self.__display_game_message(
            self.__drawer_name+" has been chosen as drawer")
        while True:
            request_reply = self._game_controller.guesser_listener(
                self._GUI.get_username())

            if not request_reply:
                continue

            reply_code = request_reply[0]
            print(reply_code)

            if reply_code == ApplicationCode.BROADCAST_IMAGE_RECEIVED:
                print("Enable guessing")
                self.__start_guessing()
            elif reply_code == ApplicationCode.BROADCAST_ANSWER:
                reply_msg = request_reply[1]
                self.__display_user_message(
                    reply_msg['username'], reply_msg['message'])
            elif reply_code == ApplicationCode.GIVE_HINT and not self.__is_drawer:
                hinted_keyword = request_reply[1]
                self.__display_header(hinted_keyword)
            elif reply_code == ApplicationCode.RIGHT_GUESS_FOUND:
                reply_msg = request_reply[1]
                keyword = reply_msg['keyword']
                right_guesser = reply_msg['right_guesser']
                scores_earned = reply_msg['scores_earned']
                players_dict = reply_msg['players_dict']

                self.__display_header(keyword)
                self.__display_scoreboard(players_dict, self.__drawer_name)
                self.__display_game_message(
                    right_guesser + " made the right guess!")
                self.__display_game_message(
                    right_guesser + " earn " + str(scores_earned['guesser']) + " points")
                self.__display_game_message(
                    self.__drawer_name + " earn " + str(scores_earned['drawer']) + " points")
                # self.__display_game_message("New round is starting...")

                self.__stop_countdown()
                # reply_msg = self._game_controller.listen_for_role_assignment()
                # self._window.after(5000, self.__start_new_round, reply_msg)
                self._window.after(15000, self.__end_game)

            elif reply_code == ApplicationCode.TIME_OUT_ROUND_END:
                keyword = request_reply[1]
                self.__display_header(keyword)
                self.__display_game_message("Time out. No one earn any points")

                self.__stop_countdown()
                # reply_msg = self._game_controller.listen_for_role_assignment()
                # self._window.after(5000, self.__start_new_round, reply_msg)
                self._window.after(15000, self.__end_game)

    def __start_guessing(self):
        cur_dir = os.getcwd()
        save_dir = './Paint/saves/receive/'
        filename = 'image' + '_' + self._GUI.get_username() + '.png'
        image_path = os.path.join(cur_dir, save_dir, filename)

        self.__display_image(image_path)
        self.__enable_answering()

        keyword_display = self.__obc_keyword
        self.__display_header(keyword_display)

        self.__count_down()

    def from_drawer_init(self):
        print("init")
        self._window.after(100, self.__display_image_from_drawer)

    def __display_image_from_drawer(self):
        print("display image")

        cur_dir = os.getcwd()
        save_dir = './Paint/saves/send/'
        filename = 'image' + '_' + self._GUI.get_username() + '.png'
        image_path = os.path.join(cur_dir, save_dir, filename)
        self.__display_image(image_path)
        self.__display_header("Other players are guessing")

        self.__count_down()

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

        if self.__clock >= 0 and self.__counting_down:
            self._window.after(1000, self.__count_down)

            if self.__clock <= 5:
                self.__timer_label.config(fg="red")

            if self.__clock == SystemConst.HINT_TIME:
                print("Request hint")
                self._game_controller.request_hint()
        elif self.__clock <= 0:
            print("Time out")
            if self.__is_drawer:
                self._game_controller.guesser_time_out()

    def __stop_countdown(self):
        self.__counting_down = False

    def __start_new_round(self, reply_msg):
        self._window.destroy()
        self._GUI.display_game_window(reply_msg)

    def __end_game(self):
        self._game_controller.logout()
        self._window.destroy()
        self._GUI.get_game_window().destroy()

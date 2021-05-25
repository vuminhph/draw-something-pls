from classes.GameController import GameController
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role
from classes.Timer import Duration

# import all the required modules
from tkinter import *
from tkinter import font
from tkinter import ttk
# from PIL import Image

import time
from _thread import *

# import threading
# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, host: str, port: int):
        self.__game_controller = GameController(host, port)

        # chat window which is currently hidden
        self.__game_window = Tk()
        self.__game_window.withdraw()

        login_window = LoginWindow(self.__game_controller)
        login_window.set_GUI(self)

        self.__game_window.mainloop()

    def set_username(self, username: str):
        self.__username = username

    def display_waiting_window(self):
        waiting_window = WaitingWindow(self.__game_controller)
        waiting_window.set_GUI(self)

    def display_game_window(self):
        # Game window
        self.__game_window.deiconify()
        self.__game_window.title("GAME ROOM #1")
        self.__game_window.resizable(width=False,
                                     height=False)
        self.__game_window.configure(width=1024,
                                     height=768,
                                     bg="#17202A")

        self.__labelHead = Label(self.__game_window,
                                 bg="#17202A",
                                 fg="#EAECEE",
                                 text=self.__username,		# Countdown placement
                                 font="Helvetica 13 bold",
                                 pady=5)
        self.__labelHead.place(relwidth=1)

        self.__line = Label(self.__game_window,
                            width=450,
                            bg="#ABB2B9")
        self.__line.place(relwidth=1,
                          rely=0.07,
                          relheight=0.01)

        # Chat room
        self.__chatRoom = Text(self.__game_window,
                               width=20,
                               height=2,
                               bg="#17202A",
                               fg="#EAECEE",
                               font="Helvetica 14",
                               padx=1,
                               pady=1)
        self.__chatRoom.place(relheight=0.745,
                              relwidth=0.3,
                              rely=0.08)

        # Scroll bar for chat room
        scrollbar = Scrollbar(self.__chatRoom)
        scrollbar.place(relheight=1,
                        relx=0.94)
        scrollbar.config(command=self.__chatRoom.yview)

        # Picture room
        pictName = './images/@NVH-play.png'  # Define picture pathname
        self.__pict = PhotoImage(file=pictName).subsample(2)
        self.__pictureRoom = Label(self.__game_window, image=self.__pict)
        self.__pictureRoom.place(relheight=0.745,
                                 relwidth=0.7,
                                 relx=0.3,
                                 rely=0.08)

        self.__labelBottom = Label(self.__game_window,
                                   bg="#ABB2B9",
                                   height=80)
        self.__labelBottom.place(relwidth=1,
                                 rely=0.825)

        self.__entryMsg = Entry(self.__labelBottom,
                                bg="#2C3E50",
                                fg="#EAECEE",
                                font="Helvetica 13")
        self.__entryMsg.place(relwidth=0.74,
                              relheight=0.06,
                              rely=0.008,
                              relx=0.011)
        self.__entryMsg.focus()

        # create a Send Button
        self.__buttonMsg = Button(self.__labelBottom,
                                  text="Send",
                                  font="Helvetica 10 bold",
                                  width=20,
                                  bg="#ABB2B9",
                                  command=lambda: self.__send_message(self.__entryMsg.get()))
        self.__buttonMsg.place(relx=0.77,
                               rely=0.008,
                               relheight=0.06,
                               relwidth=0.22)
        self.__chatRoom.config(cursor="arrow")

        self.__chatRoom.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def __send_message(self, msg):
        self.__chatRoom.config(state=DISABLED)
        self.msg = msg
        self.__entryMsg.delete(0, END)
        # snd = threading.Thread(target=Communicator.send_message)
        # snd.start()

    # function to receive messages
    # TODO

    # function to send messages
    # TODO


class LoginWindow:
    def __init__(self, game_controller: GameController):
        self.__game_controller = game_controller

        self.__window = Toplevel()
        # set the title
        self.__window.title("Login")
        self.__window.resizable(width=False,
                                height=False)
        self.__window.configure(width=400,
                                height=300)
        # create login request Label
        label_instruct = Label(self.__window,
                               text="Please login to continue",
                               justify=CENTER,
                               font="Helvetica 14 bold")

        label_instruct.place(relheight=0.15,
                             relwidth=1,
                             rely=0.07)

        # create a Label username
        label_username = Label(self.__window,
                               text="Username: ",
                               font="Helvetica 12")

        label_username.place(relheight=0.2,
                             relx=0.1,
                             rely=0.3)
        self.__entry_username = Entry(self.__window,
                                      font="Helvetica 14")

        self.__entry_username.place(relwidth=0.4,
                                    relheight=0.12,
                                    relx=0.35,
                                    rely=0.3)

        # set the focus of the curser
        self.__entry_username.focus()

        # create a Label password
        label_password = Label(self.__window,
                               text="Password: ",
                               font="Helvetica 12")

        label_password.place(relheight=0.2,
                             relx=0.1,
                             rely=0.45)

        # create a entry box for typing the password
        self.__entry_password = Entry(self.__window,
                                      show="\u2022",
                                      width=15)

        self.__entry_password.place(relwidth=0.4,
                                    relheight=0.12,
                                    relx=0.35,
                                    rely=0.45)

        # create a Continue Button along with action
        self.go = Button(self.__window,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.__login())

        self.go.place(relx=0.4,
                      rely=0.6)

    def __login(self):
        # Send a login request to the server and check if login is successful

        username = self.__entry_username.get()
        password = self.__entry_password.get()

        is_login_success = self.__game_controller.login(
            username, password)

        if is_login_success:
            self.__go_ahead(username)
        else:
            # Display error message
            label_error = Label(self.__window,
                                text="Login unsuccessful. Please try again!",
                                justify=CENTER,
                                font="Helvetica 14",
                                fg="red")

            label_error.place(relheight=0.15,
                              relwidth=1,
                              rely=0.8)

    def set_GUI(self, GUI: GUI):
        self.__GUI = GUI

    def __go_ahead(self, username: str):
        # If login is successful, then destroy login window to the next window
        self.__window.destroy()
        time.sleep(1)
        self.__GUI.set_username(username)
        self.__GUI.display_waiting_window()


class WaitingWindow:
    # constructor method
    def __init__(self, game_controller: GameController):
        self.__game_controller = game_controller

        self.__window = Toplevel()

        # Main wait window
        self.__window.title("Please wait...")
        self.__window.resizable(width=False,
                                height=False)
        self.__window.configure(width=400,
                                height=300)

        # Label
        self.__label = Label(self.__window,
                             text="Waiting for other players...",
                             font="Tamoha 14 bold")
        self.__label.place(relwidth=1,
                           relheight=0.2)

        # Waiting logo
        self.__frame_count = 8
        self.__wait_logo = [PhotoImage(file='./images/waiting.gif',
                                       format='gif -index %i' % (i))
                            for i in range(self.__frame_count)]
        self.__wait_logo_label = Label(self.__window)
        self.__wait_logo_label.place(relheight=0.5,
                                     relwidth=1,
                                     rely=0.25)

        # Countdown placement
        self.__clock = self.__game_controller.request_clock_value()
        self.__timer = StringVar()
        self.__timer.set(str(self.__clock))  # The countdown timer
        self.__countdown_timer = Label(self.__window,
                                       textvariable=self.__timer,
                                       font="Helvetica 14")
        self.__countdown_timer.place(relwidth=1,
                                     relheight=0.25,
                                     rely=0.75)

        # Set the main loop
        self.__thread_created = False
        self.__window.after(0, self.__update_frame, 0)
        self.__window.mainloop()

    def __update_frame(self, i):
        try:
            if not self.__thread_created:
                start_new_thread(self.__count_down, ())
                self.__thread_created = True

            frame = self.__wait_logo[i]
            i += 1
            if i == self.__frame_count:
                i = 0

            self.__wait_logo_label.configure(image=frame)
            self.__window.after(100, self.__update_frame, i)
        except:
            pass

    def set_GUI(self, GUI: GUI):
        self.__GUI = GUI

    def __count_down(self):
        while self.__clock >= 0:
            time.sleep(1)
            self.__clock -= 1
            self.__timer.set(str(self.__clock))

            if self.__clock == 0:
                reply_msg = self.__game_controller.start_game_request()
                if reply_msg['code'] == ApplicationCode.CONTINUE_WAITING:
                    self.__clock = Duration.WAITING_FOR_PLAYERS
                elif reply_msg['code'] == ApplicationCode.GAME_ASSIGN_ROLE:
                    # print the player's role
                    if reply_msg['role'] == Role.Drawer:
                        print('You have been assigned the role of Drawer')
                    elif reply_msg['role'] == Role.Guesser:
                        print('You have been assigned the role of Guesser')
                    self.__window.destroy()
                    time.sleep(1)

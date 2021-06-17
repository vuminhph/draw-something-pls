from classes.Client.windows.DisplayWindow import DisplayWindow
import classes.Client.GUI

from tkinter import *
from tkinter import messagebox
import time


class LoginWindow(DisplayWindow):
    def __init__(self, GUI):
        super().__init__(GUI)

        # set the title
        self._window.title("Login")
        self._window.resizable(width=False,
                               height=False)
        self._window.configure(width=400,
                               height=300)
        # create login request Label
        label_instruct = Label(self._window,
                               text="Please login to continue",
                               justify=CENTER,
                               font="Helvetica 14 bold")

        label_instruct.place(relheight=0.15,
                             relwidth=1,
                             rely=0.07)

        # create a Label username
        label_username = Label(self._window,
                               text="Username: ",
                               font="Helvetica 12")

        label_username.place(relheight=0.2,
                             relx=0.1,
                             rely=0.3)
        self.__entry_username = Entry(self._window,
                                      font="Helvetica 14")

        self.__entry_username.place(relwidth=0.4,
                                    relheight=0.12,
                                    relx=0.35,
                                    rely=0.3)

        # set the focus of the curser
        self.__entry_username.focus()

        # create a Label password
        label_password = Label(self._window,
                               text="Password: ",
                               font="Helvetica 12")

        label_password.place(relheight=0.2,
                             relx=0.1,
                             rely=0.45)

        # create a entry box for typing the password
        self.__entry_password = Entry(self._window,
                                      show="\u2022",
                                      width=15)

        self.__entry_password.place(relwidth=0.4,
                                    relheight=0.12,
                                    relx=0.35,
                                    rely=0.45)

        # create a Continue Button along with action
        self.go = Button(self._window,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=self.__login)

        self.go.place(relx=0.4,
                      rely=0.6)

        # Press Enter to log in
        self._window.bind('<Return>', lambda e: self.__login())
        self._window.mainloop()

    def __login(self):
        # Send a login request to the server and check if login is successful

        username = self.__entry_username.get()
        password = self.__entry_password.get()

        is_login_success = self._game_controller.login(
            username, password)

        if is_login_success:
            self.__go_ahead(username)
        else:
            # Display error message
            label_error = Label(self._window,
                                text="Login unsuccessful. Please try again!",
                                justify=CENTER,
                                font="Helvetica 14",
                                fg="red")

            label_error.place(relheight=0.15,
                              relwidth=1,
                              rely=0.8)

    def __go_ahead(self, username: str):
        # If login is successful, then destroy login window to the next window
        self._window.destroy()
        time.sleep(1)
        self._GUI.set_username(username)
        self._GUI.display_waiting_window()

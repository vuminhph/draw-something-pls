from tkinter import *
from tkinter.scrolledtext import ScrolledText
import time

from classes.windows.DisplayWindow import DisplayWindow
import classes.enums.ApplicationCode
import classes.enums.Role
import classes.Timer
import classes.GUI

FONT = ("Consolas", 20)
LOGO = './images/DSL_logo.png'

class FirstWindow(DisplayWindow):
    def __init__(self, GUI):
        super().__init__(GUI)

        self._window.resizable(False, False)
        self._window.title('Draw Something, Please')

        # creating a container
        container = Frame(self._window)
        container.pack(side = "top", fill = "both", expand = True)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, LoginPage, RulePage):

            frame = F(container, self, GUI)
            frame.configure(width=1280, height=720)

            # initializing frame of that object from
            # home page, login page, rule page respectively with for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(HomePage)
        self._window.mainloop()

    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(DisplayWindow, Frame):
    def __init__(self, parent, controller, GUI):
        super(HomePage, self).__init__(GUI)
        super(HomePage, self)._close()
        Frame.__init__(self, parent)

        # Logo
        self.__logo = PhotoImage(file=LOGO)
        self.__logo_label = Label(self,
                                  image=self.__logo)
        self.__logo_label.place(relx=0.5,
                                rely=0.3,
                                anchor=CENTER)

        # Login button
        self.__login_btn = Button(self, text="Log in", font=FONT, cursor="hand2", bg="#126E82", fg="white", borderwidth=3,
                                  command = lambda : controller.show_frame(LoginPage))

        self.__login_btn.place(relwidth=0.2,
                               relx=0.4,
                               rely=0.65)

        # Game rule button
        self.__rule_btn = Button(self, text="Game Rule", font=FONT, cursor="hand2", bg="#51C4D3", borderwidth=3,
                                 command = lambda : controller.show_frame(RulePage))

        self.__rule_btn.place(relwidth=0.2,
                              relx=0.4,
                              rely=0.75)

class RulePage(DisplayWindow, Frame):
    def __init__(self, parent, controller, GUI):
        super(RulePage, self).__init__(GUI)
        super(RulePage, self)._close()
        Frame.__init__(self, parent)

        # Label
        self.__rule_label = Label(self,
                                  text ="Game Rule",
                                  font = "Consolas 40 bold",
                                  fg="#126E82",
                                  justify=CENTER)
        self.__rule_label.place(relheight=0.15,
                                relwidth=1,
                                rely=0.02)

        # Rule
        self.__rule = ScrolledText(self,
                                   font="Consolas 16",
                                   wrap=WORD)
        self.__rule.insert(INSERT,
            """\
• In a game, players are assigned to a role of either drawer or guesser.\n
• The drawer is given a word or phrase. He will have some time to make a drawing \
that illustrate to others what the word or phrase is.\n
• The guessers have some time to find out the word or phrase by sending their \
answers as text messages. They can give as many responses as possible until \
the correct answer is found, or the time is up.\n
• The first guesser with the correct answer will be rewarded points according \
to the time he took to answer. The drawer is also rewarded higher points than \
the guesser. If no one can answer correctly, everybody gets 0 point.\n
• When all players have already taken the role of drawer, the player with the highest score wins.\
            """
        )
        self.__rule.configure(state=DISABLED)
        self.__rule.place(relheight=0.7,
                          relwidth=0.9,
                          relx=0.05,
                          rely=0.2)

        # Return home page
        self.__back_btn = Button(self, text="<", font="Consolas 40", cursor="hand2", relief=FLAT,
                                 command = lambda : controller.show_frame(HomePage))

        self.__back_btn.place(relwidth=0.05,
                              relheight=0.1,
                              relx=0.01,
                              rely=0.02)        

class LoginPage(DisplayWindow, Frame):
    def __init__(self, parent, controller, GUI):
        super(LoginPage, self).__init__(GUI)
        super(LoginPage, self)._close()
        Frame.__init__(self, parent)

        # Logo
        self.__logo = PhotoImage(file=LOGO).subsample(2)
        self.__logo_label = Label(self,
                                  image=self.__logo)
        self.__logo_label.place(relx=0.25,
                                rely=0.5,
                                anchor=CENTER)

        # create login instruct Label
        label_instruct = Label(self,
                               text="Please login to continue",
                               justify=CENTER,
                               font="Consolas 30 bold",
                               fg="#126E82")

        label_instruct.place(relwidth=0.45,
                             relheight=0.15,
                             relx=0.5,
                             rely=0.25)

        # Username
        self.__label_username = Label(self,
                                      text="Username: ",
                                      font=FONT)
        self.__label_username.place(relheight=0.05,
                                    relx=0.5,
                                    rely=0.4)

        self.__entry_username = Entry(self,
                                      font=FONT)
        self.__entry_username.place(relwidth=0.3,
                                    relheight=0.05,
                                    relx=0.65,
                                    rely=0.4)

        # set the focus of the curser
        self.__entry_username.focus()

        # Password
        self.__label_password = Label(self,
                                      text="Password: ",
                                      font=FONT)

        self.__label_password.place(relheight=0.05,
                                    relx=0.5,
                                    rely=0.5)

        self.__entry_password = Entry(self,
                                      show="\u2022",
                                      font=FONT)
        self.__entry_password.place(relwidth=0.3,
                                    relheight=0.05,
                                    relx=0.65,
                                    rely=0.5)

        # Log in continue
        self.__log_in_btn = Button(self, text ="CONTINUE", font = FONT, cursor="hand2", bg="#51C4D3", borderwidth=3,
                                   command = lambda: self.__login(controller))

        self.__log_in_btn.place(relwidth=0.2,
                                relx=0.7,
                                rely=0.6)

        # Press Enter to log in
        self.bind('<Return>', lambda e: self.__login(controller))

        # Return home page
        self.__back_btn = Button(self, text="<", font="Consolas 40", cursor="hand2", relief=FLAT,
                                 command = lambda: controller.show_frame(HomePage))

        self.__back_btn.place(relwidth=0.05,
                              relheight=0.1,
                              relx=0.01,
                              rely=0.02)

    def __login(self, controller):
        # Send a login request to the server and check if login is successful

        username = self.__entry_username.get()
        password = self.__entry_password.get()

        is_login_success = self._game_controller.login(username, password)

        if is_login_success:
            self.__go_ahead(username, controller)
        else:
            # Display error message
            label_error = Label(self,
                                text="Login unsuccessful. Please try again!",
                                justify=CENTER,
                                font=FONT,
                                fg="red")

            label_error.place(relheight=0.15,
                              relwidth=0.45,
                              relx=0.5,
                              rely=0.7)

    def __go_ahead(self, username: str, controller):
        # If login is successful, then destroy login window to the next window
        controller._window.destroy()
        time.sleep(1)
        self._GUI.set_username(username)
        self._GUI.display_waiting_window()

# app = FirstWindow()
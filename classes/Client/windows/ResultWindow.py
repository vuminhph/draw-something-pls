from classes.Client.windows.DisplayWindow import DisplayWindow
from tkinter import *


class ResultWindow(DisplayWindow):
    def __init__(self, GUI):
        super().__init__(GUI)
        # self._window = Toplevel()

        # Set window
        self._window.title("Result")
        self._window.resizable(width=False,
                               height=False)
        self._window.configure(width=500,
                               height=500)

        # Show results
        self.__results__label = Label(self._window,
                                      text="FINAL RESULTS",
                                      font=("Consolas", 30, "bold"))
        self.__results__label.place(relheight=0.15,
                                    relwidth=1)

        self.__results__dict = Text(self._window,
                                    font=("Consolas", 20),
                                    state=DISABLED)
        # self.__results__dict.insert(END, "Hoang: 10\n\nMinh: 20\n\nHung: 30\n\nPhuc: 40\n\nDuong: 50\n\nHong Anh: 60\n\n")
        # self.__results__dict.configure(state=DISABLED)
        self.__results__dict.place(rely=0.15,
                                   relheight=0.7)

        # Announce winner
        self.__winner = StringVar()
        # self.__winner.set("The winner is Hong Anh!")

        self.__winner__announce = Label(self._window,
                                        textvariable=self.__winner,
                                        font=("Consolas", 25, "bold"),
                                        fg="red",
                                        justify=CENTER)
        self.__winner__announce.place(rely=0.85,
                                      relwidth=1,
                                      relheight=0.15)

        # self._window.mainloop()
        # pass

    def __get_final_result(self, gameWinner: str, scoreboard: dict):
        self.__results__dict.configure(state=NORMAL)
        for user in scoreboard.keys():
            score = scoreboard[user]
            self.__results__dict.insert(END, user + ': ', score + '\n\n')
        self.__results__dict.configure(state=DISABLED)

        self.__winner.set("The winner is: " + gameWinner + "!")
        # pass


result = ResultWindow()

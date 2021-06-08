from classes.windows.DisplayWindow import DisplayWindow
from tkinter import *

class ResultWindow(DisplayWindow):
    def __init__(self, GUI):
        super().__init__(GUI)

        # Set window
        self._window.title("Result")
        self._window.resizable(width=False,
                               height=False)
        self._window.configure(width=300,
                               height=500)
        
        # Show results        
        self.__results__label = Label(self._window,
                                      text="FINAL RESULTS",
                                      font=("Consolas", 35, "bold"))
        self.__results__label.place() #TODO

        self.__results__dict = Text(self._window,
                                    state=DISABLED,
                                    font=("Consolas", 35))
        self.__results__dict.place() #TODO

        # Announce winner
        self.__winner = StringVar()

        self.__winner__announce = Label(self._window,
                                        textvariable=self.__winner__announce,
                                        font=("Consolas", 40, "bold"),
                                        fg="red")
        self.__winner__announce.place() #TODO
        pass

    def __get_final_result(self, gameWinner, scoreboard:dict):
        self.__results__dict.configure(state=NORMAL)
        for user in scoreboard.keys():
            score = scoreboard[user]
            self.__results__dict.insert(END, user + ': ', score + '\n\n')
        self.__results__dict.configure(state=DISABLED)

        self.__winner.set("The winner is: " + gameWinner + "!")
        pass
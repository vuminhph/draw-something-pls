from classes.windows.DisplayWindow import DisplayWindow
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role
from classes.Timer import Duration
import classes.GUI

# import all the required modules
from tkinter import *
# from PIL import Image

import time
from _thread import *


class WaitingWindow(DisplayWindow):
    # constructor method
    def __init__(self, GUI):
        super().__init__(GUI)

        # Main wait window
        self._window.title("Please wait...")
        self._window.resizable(width=False,
                               height=False)
        self._window.configure(width=400,
                               height=300)

        # Label
        self.__label = Label(self._window,
                             text="Waiting for other players...",
                             font="Tamoha 14 bold")
        self.__label.place(relwidth=1,
                           relheight=0.2)

        # Waiting logo
        self.__frame_count = 8
        self.__wait_logo = [PhotoImage(file='./images/waiting.gif',
                                       format='gif -index %i' % (i))
                            for i in range(self.__frame_count)]
        self.__wait_logo_label = Label(self._window)
        self.__wait_logo_label.place(relheight=0.5,
                                     relwidth=1,
                                     rely=0.25)

        # Countdown placement
        self.__clock = self._game_controller.request_clock_value()
        self.__timer = StringVar()
        self.__timer.set(str(self.__clock))  # The countdown timer
        self.__countdown_timer = Label(self._window,
                                       textvariable=self.__timer,
                                       font="Helvetica 14")
        self.__countdown_timer.place(relwidth=1,
                                     relheight=0.25,
                                     rely=0.75)

        # Set the main loop
        self.__thread_created = False
        self._window.after(0, self.__update_frame, 0)

        start_new_thread(self.__count_down, ())
        self._window.mainloop()

    def __update_frame(self, i):
        frame = self.__wait_logo[i]
        i += 1
        if i == self.__frame_count:
            i = 0

        self.__wait_logo_label.configure(image=frame)
        self._window.after(100, self.__update_frame, i)

    def __count_down(self):
        while self.__clock >= 0:
            time.sleep(1)
            self.__clock -= 1
            self.__timer.set(str(self.__clock))

            if self.__clock == 0:
                reply_msg = self._game_controller.start_game_request()
                if reply_msg['code'] == ApplicationCode.CONTINUE_WAITING:
                    self.__clock = Duration.WAITING_FOR_PLAYERS
                elif reply_msg['code'] == ApplicationCode.GAME_ASSIGN_ROLE:
                    self._window.after(50, self.__start_game, (reply_msg))
                    return

    def __start_game(self, reply_msg):
        self._window.destroy()
        time.sleep(1)
        self._GUI.display_game_window(reply_msg)

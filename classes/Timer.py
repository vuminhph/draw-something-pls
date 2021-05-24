import time
from utils import singleton


@singleton
class Timer:
    def __init__(self, t):
        self.is_countdown_finished = False
        self.__time_start = self.__time_cur = t

    def start_countdown(self):
        # countdown

        self.__time_cur = self.__time_start

        while self.__time_cur:
            time.sleep(1)
            self.__time_cur -= 1

        self.is_countdown_finished = True

    def restart_countdown(self):
        self.is_countdown_finished = False
        self.start_countdown()

    def get_curtime(self):
        return self.__time_cur

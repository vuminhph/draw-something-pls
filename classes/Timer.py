import time
from utils import singleton


@singleton
class Timer:
    def __init__(self, t):
        self.__time_start = self.__time_cur = t

    def start_countdown(self):
        # Blocking countdown

        self.__time_cur = self.__time_start

        while self.__time_cur:
            time.sleep(1)
            self.__time_cur -= 1
            print('Current time:', self.__time_cur, end='\r')

    def get_curtime(self):
        return self.__time_cur


class Duration():
    WAITING_FOR_PLAYERS = 30

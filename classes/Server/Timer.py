from threading import Timer as timer
import time
import sys
from _thread import *
# from utils import singleton, run_once


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


class Timer:
    def __init__(self, t):
        self.__time_start = self.__time_cur = t
        self.__run_clock = True

    # @run_once
    def start_countdown(self):
        self.__run_clock = True
        self.__time_cur = self.__time_start
        self.__count_down()

    def __count_down(self):
        if self.__run_clock:
            clock_text = str(round(self.__time_cur, 1)).zfill(2)
            print(f'Current time: {clock_text}', end='\r')
            self.__time_cur -= 0.1

            if self.__time_cur > 0:
                t = timer(0.1, self.__count_down)
                t.start()
            else:
                self.start_countdown()

    def get_curtime(self):
        return self.__time_cur

    def stop_clock(self):
        self.__run_clock = False

# For testing


def func(clock):
    clock.start_countdown()
    time.sleep(5)
    print('hi')


def stop_func(thread, clock):
    thread = start_new_thread(func, (clock,))
    # print('ok')


if __name__ == "__main__":
    clock = Timer(5)
    thread = start_new_thread(func, (clock,))
    while True:
        pass
        # time.sleep(15)
        # thread = start_new_thread(func, (clock,))
        # thread = None

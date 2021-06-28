from classes.Client.Communicator import Communicator
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.SystemConst import SystemConst

from threading import Timer
import os
import json
import base64
import math
import time


class GameController:
    def __init__(self, host: str, port: int):
        self.__communicator = Communicator(host, port)

        self.__image_pkgs = []  # TODO: reset every round
        self.__num_of_packages = 0  # TODO: reset every round
        self.__package_wait_timeout_started = False  # TODO: reset every round
        self.__waiting_for_packages = True  # TODO: reset every round

    def login(self, username: str, password: str):
        # Send a login request to the server and check if login is successful

        # send login request msg
        send_msg = json.dumps(
            {'code': ApplicationCode.LOGIN_REQUEST, 'username': username, 'password': password})
        self.__communicator.send_message(send_msg)

        # receive reply from server
        reply_msg = self.__communicator.receive_message()
        if reply_msg['code'] == ApplicationCode.LOGIN_SUCCESS:
            return True
        else:
            return False

    def request_clock_value(self):
        # Request the server's waiting clock value

        # Returns:
        # -- the current countdown time from server

        send_msg = json.dumps({'code': ApplicationCode.WAIT_TIME_REQUEST})
        self.__communicator.send_message(send_msg)

        # receive reply from server
        reply_msg = self.__communicator.receive_message()
        return reply_msg['current_time']

    def start_game_request(self):
        # Signal the server to start the game, receive a role assignment if game is ready to start
        # or continue waiting signal

        # Returns:
        # -- the reply message json

        send_msg = json.dumps({'code': ApplicationCode.GAME_START_REQUEST})
        self.__communicator.send_message(send_msg)

        return self.listen_for_role_assignment()

    def listen_for_role_assignment(self):
        # receive reply from server
        reply_msg = self.__communicator.receive_message()
        if reply_msg['code'] == ApplicationCode.GAME_ASSIGN_ROLE or reply_msg['code'] == ApplicationCode.CONTINUE_WAITING:
            return reply_msg

    def send_image(self, username, time_left):
        # Called by the drawer window, sends the result image to the server
        # Returns players_dict if server receive image successfully

        cur_dir = os.getcwd()
        save_dir = './Paint/saves/send/'
        filename = 'image' + '_' + username + '.png'
        image_path = os.path.join(cur_dir, save_dir, filename)

        with open(image_path, "rb") as image:
            f = base64.b64encode(image.read()).decode('utf-8')
            image.close()

            msg = {'code': ApplicationCode.SEND_IMAGE, 'image': ''}
            overhead = json.dumps(msg)

            image_size = len(f)
            overhead_size = len(overhead)

            num_of_packages = 1

            if overhead_size + image_size > SystemConst.MESSAGE_SIZE:
                num_of_packages = math.ceil(image_size / (
                    SystemConst.MESSAGE_SIZE - overhead_size))

            msg = {}
            msg['code'] = ApplicationCode.SEND_IMAGE_REQUEST
            msg['num_pkgs'] = num_of_packages
            msg['time_left'] = time_left
            print("Number of packages: ", num_of_packages)

            # request the server to send image
            send_msg = json.dumps(msg)
            self.__communicator.send_message(send_msg)

            # receive reply from server
            print(f)
            print(num_of_packages)
            reply_msg = self.__communicator.receive_message()

            if reply_msg['code'] == ApplicationCode.READY_TO_RECEIVE_IMAGE:
                print("ok")
                self.__send_image_packages(f, num_of_packages)
                print("Image sent")

                # listen for receive status
                reply_msg = self.__communicator.receive_message()
                if reply_msg['code'] == ApplicationCode.IMAGE_RECEIVED:
                    return reply_msg['players_dict']
                elif reply_msg['code'] == ApplicationCode.IMAGE_PACKAGES_LOSS:
                    self.__send_image_packages(f, num_of_packages)
                else:
                    return False

            else:
                print("couldn't happen")
                return False

    def __send_image_packages(self, f, num_of_packages):
        msg = {}
        msg['code'] = ApplicationCode.SEND_IMAGE
        # Split image base64 string to fit packages
        f_splitted = self.__split_str_n_times(f, num_of_packages)
        for p in f_splitted:
            print("payload packed")
            msg['image'] = p
            send_msg = json.dumps(msg)
            self.__communicator.send_message(send_msg)

    def guesser_listener(self, username):
        # Receive the broadcast request and save number of packages
        # Returns: True when image has been received successfully

        reply_msg = self.__communicator.receive_message()
        if reply_msg['code'] == ApplicationCode.BROADCASE_IMAGE_REQUEST:
            self.__num_of_packages = reply_msg['num_pkgs']
            send_msg = json.dumps(
                {'code': ApplicationCode.READY_TO_BROADCAST_IMAGE})
            self.__communicator.send_message(send_msg)

            # Receive the broadcasted image packages
            for i in range(self.__num_of_packages):
                if not self.__waiting_for_packages:
                    break

                reply_msg = self.__communicator.receive_message()
                if reply_msg['code'] == ApplicationCode.BROADCAST_IMAGE:
                    self.__image_pkgs.append(reply_msg['image'])

                    num_pkgs_received = len(self.__image_pkgs)
                    print("number of packages received: ", num_pkgs_received)

                    if num_pkgs_received == self.__num_of_packages:
                        print("All packages received")
                        cur_dir = os.getcwd()
                        save_dir = './Paint/saves/receive/'
                        filename = 'image' + '_' + username + '.png'
                        image_path = os.path.join(cur_dir, save_dir, filename)

                        with open(image_path, "wb+") as image:
                            image_str = base64.b64decode(
                                ''.join(self.__image_pkgs))
                            # print(image_str)
                            image.write(image_str)

                        send_msg = json.dumps(
                            {'code': ApplicationCode.BROADCAST_IMAGE_RECEIVED})
                        self.__communicator.send_message(send_msg)

                        return (ApplicationCode.BROADCAST_IMAGE_RECEIVED, '')

                    # Set a timeout to wait for all packages to be sent
                    if not self.__package_wait_timeout_started:
                        self.__package_wait_timeout_started = True
                        timer = Timer(SystemConst.WAIT_IMAGE_TIMEOUT,
                                      self.__image_receive_checkup, ())
                        timer.start()

        elif reply_msg['code'] == ApplicationCode.BROADCAST_ANSWER:
            return (ApplicationCode.BROADCAST_ANSWER, reply_msg)
        elif reply_msg['code'] == ApplicationCode.RIGHT_GUESS_FOUND:
            return (ApplicationCode.RIGHT_GUESS_FOUND, reply_msg)
        elif reply_msg['code'] == ApplicationCode.GIVE_HINT:
            return (ApplicationCode.GIVE_HINT, reply_msg['hinted_keyword'])
        elif reply_msg['code'] == ApplicationCode.GAME_ASSIGN_ROLE:
            return (ApplicationCode.GIVE_HINT, reply_msg)
        else:
            return False

    def __image_receive_checkup(self):
        # Check to see if all packages have been received

        if len(self.__image_pkgs) != self.__num_of_packages:
            send_msg = json.dumps(
                {'code': ApplicationCode.BROADCAST_IMAGE_PACKAGES_LOSS})
            self.__communicator.send_message(send_msg)
            self.__waiting_for_packages = False

    def __split_str_n_times(self, string, n):
        # splits a string up into list of n elements

        # Arguments:
        # -- string: string to be split
        # -- n: number of times element in returned list
        # Returns:
        # -- list: list of n elementes splitted from the string

        list = []
        char_size = len(string) // n

        index = 0
        sub_str = ''

        for i, c in enumerate(string):
            sub_str += c
            index += 1

            if index == char_size:
                list.append(sub_str)
                index = 0
                sub_str = ''

            elif i == len(string) - 1:
                list[-1] += sub_str

        return list

    def send_message(self, username, message, time_left):
        # Sends the guesser's answer to the server
        send_msg = json.dumps(
            {'code': ApplicationCode.SEND_ANSWER,
             'username': username,
             'message': message,
             'time_left': time_left})
        self.__communicator.send_message(send_msg)

    def request_hint(self):
        # Request server for a hint
        send_msg = json.dumps({'code': ApplicationCode.REQUEST_HINT})
        self.__communicator.send_message(send_msg)

    def reset_round(self):
        self.__image_pkgs = []
        self.__num_of_packages = 0
        self.__package_wait_timeout_started = False
        self.__waiting_for_packages = True

    def logout(self):
        send_msg = json.dumps({'code': ApplicationCode.LOGOUT})
        self.__communicator.send_message(send_msg)

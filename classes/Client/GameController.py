from classes.Client.Communicator import Communicator
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.SystemConst import SystemConst

import os
import json
import base64
import math


class GameController:
    def __init__(self, host: str, port: int):
        self.__communicator = Communicator(host, port)

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

        # receive reply from server
        reply_msg = self.__communicator.receive_message()
        return reply_msg

    def send_picture(self, username):
        # Called by the drawer window, sends the result image to the server

        cur_dir = os.getcwd()
        save_dir = './Paint/saves/send/'
        filename = 'image' + '_' + username + '.png'
        image_path = os.path.join(cur_dir, save_dir, filename)

        with open(image_path, "rb") as image:
            f = str(base64.b64encode(image.read()))
            msg = {'code': ApplicationCode.SEND_IMAGE, 'image': ''}
            overhead = json.dumps(msg)

            image_size = len(f)
            overhead_size = len(overhead)

            num_of_packages = 1

            if overhead_size + image_size > SystemConst.MESSAGE_SIZE:
                num_of_packages = math.ceil(image_size / (
                    SystemConst.MESSAGE_SIZE - overhead_size))

            msg['code'] = ApplicationCode.SEND_IMAGE_REQUEST
            msg['num_pkgs'] = num_of_packages
            print("Number of packages: ", num_of_packages)

            # request the server to send image
            send_msg = json.dumps(msg)
            self.__communicator.send_message(send_msg)

            # receive reply from server
            reply_msg = self.__communicator.receive_message()

            if reply_msg['code'] == ApplicationCode.READY_TO_RECEIVE_IMAGE:
                msg = {}
                msg['code'] = ApplicationCode.SEND_IMAGE
                f_splitted = self.__split_str_n_times(f, num_of_packages)
                for p in f_splitted:
                    msg['image'] = p
                    send_msg = json.dumps(msg)
                    self.__communicator.send_message(send_msg)
            print("Image sent")

    def receive_message(self):
        reply_msg = self.__communicator.receive_message()
        if reply_msg['code'] == ApplicationCode.BROADCAST_IMAGE:
            pass

    def __split_str_n_times(self, string, n):
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

    def logout(self):
        send_msg = json.dumps({'code': ApplicationCode.LOGOUT})
        self.__communicator.send_message(send_msg)

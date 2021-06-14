from Client.Communicator import Communicator
from classes.enums.ApplicationCode import ApplicationCode

import json


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

    def logout(self):
        send_msg = json.dumps({'code': ApplicationCode.LOGOUT})
        self.__communicator.send_message(send_msg)

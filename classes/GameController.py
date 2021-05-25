from classes.Communicator import Communicator
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

    def start_game(self):
        # Sends a start game signal to server

        # Returns:
        # -- the current countdown time from server

        # Signal the server to start the game
        send_msg = json.dumps({'code': ApplicationCode.GAME_START_REQUEST})
        self.__communicator.send_message(send_msg)

        # receive reply from server
        reply_msg = self.__communicator.receive_message()
        return reply_msg['cur_time']

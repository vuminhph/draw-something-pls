from classes.Communicator import Communicator

import json


class GameController:
    def __init__(self, host: str, port: int):
        self.__communicator = Communicator(host, port)

    def login(self, username: str, password: str):
        # Send a login request to the server and check if login is successful

        # send login request msg
        send_msg = json.dumps(
            {'code': '10', 'username': username, 'password': password})
        self.__communicator.send_message(send_msg)

        # receive reply from server
        login_result = self.__communicator.receive_message()
        if login_result['code'] == '100':
            return True
        else:
            return False

    def start_game(self):
        # Signal the server to start the game

        send_msg = json.dumps({'code': })

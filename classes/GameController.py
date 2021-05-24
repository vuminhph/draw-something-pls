import json

from classes.Communicator import Communicator


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

    def wait_for_players(self):
        pass
        # TODO

    def start_game(self):
        pass
        # TODO

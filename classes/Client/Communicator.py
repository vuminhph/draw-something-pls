from classes.enums.SystemConst import SystemConst

import socket
import json
import time


class Communicator:
    def __init__(self, host: str, port: int):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))

        self.RECV_SIZE = SystemConst.MESSAGE_SIZE

    def send_message(self, message: str):
        self.__socket.send(message.encode())
        print("Request sent to server: ", message)

        time.sleep(SystemConst.TIME_BETWEEN_REQUEST)

    def receive_message(self) -> str:
        reply_msg = self.__socket.recv(self.RECV_SIZE).decode('utf-8')
        print("Reply received from server: ", reply_msg)

        reply_json = json.loads(reply_msg)
        return reply_json

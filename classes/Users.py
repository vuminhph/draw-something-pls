from classes.enums.Role import Role


class User:
    def __init__(self, connection):
        self._username = None
        self.__connection = connection

    def set_username(self, username):
        self._username = username

    def get_username(self):
        return self._username

    def get_connection(self):
        return self.__connection

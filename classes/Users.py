from classes.enums.Role import Role


class User:
    def __init__(self):
        self._score = 0
        self._username = None

    def set_username(self, username):
        self._username = username

    def get_username(self):
        return self._username

    def set_score(self, score):
        self._score = score

    def get_score(self):
        return self._score

    def set_role(self, role: Role):
        self._role = role

    def get_role(self):
        return self._role


class ServerUser(User):
    def __init__(self, connection):
        super().__init__()
        self.__connection = connection

    def get_connection(self):
        return self.__connection

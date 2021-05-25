from classes.enums.Role import Role


class User:
    def __init__(self, connection):
        self.__connection = connection

    def get_connection(self):
        return self.__connection

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def assign_role(self, role: Role):
        self.__role = role

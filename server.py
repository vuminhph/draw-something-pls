from classes.Users import ServerUser as User

from classes.Timer import Timer, Duration
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role

import socket
import csv
import json
import random

from _thread import *

# Variables
MAX_PLAYERS = 5
MIN_PLAYERS = 2

UsersDatabase = {}  # Database of users and passwords information

active_users = []  # A list of currently active users
drawer_id = -1

Word_list = []  # Database of all words


def handle_request(user: User):
    # A thread serving each client

    # Arguments:
    # -- user: the client's user object

    while True:
        data = user.get_connection().recv(2048)

        if not data:
            logout(user)
            break

        received_msg = data.decode('utf-8')
        print('Received request from:',
              user.get_connection().getpeername(), ':', received_msg)
        received_msg = json.loads(received_msg)

        # LOGIN REQUEST
        if received_msg['code'] == ApplicationCode.LOGIN_REQUEST:
            return_code = login_authenticate(
                user, received_msg['username'], received_msg['password'])

            reply_msg = json.dumps({'code': return_code})
            send_reply_msg(user, reply_msg)
        #

        # JOIN ROOM REQUEST
        #  if received_msg['code'] == '20':
        # # Check if number of player exceeds the maximum number of players
            # if active_users.index(user) <= MAX_PLAYERS:
            #     reply_msg = json.dumps(
            #         {'code': ApplicationCode.JOIN_ROOM_SUCCESS, 'cur_time': timer.get_curtime()})
            # else:
            #     reply_msg = json.dumps({'code': ApplicationCode.JOIN_ROOM_ERR})
        #

        # WAIT TIME REQUEST
        if received_msg['code'] == ApplicationCode.WAIT_TIME_REQUEST:
            # A singleton timer object
            timer = Timer(Duration.WAITING_FOR_PLAYERS)

            # The first player in the room starts the waiting countdown
            if active_users.index(user) == 0:
                start_new_thread(countdown, (timer, ))

            # Reply with the current time
            reply_msg = json.dumps(
                {'code': ApplicationCode.START_WAITING, 'current_time': timer.get_curtime()})
            send_reply_msg(user, reply_msg)
        #

         # GAME START REQUEST
        if received_msg['code'] == ApplicationCode.GAME_START_REQUEST:
            if len(active_users) >= MIN_PLAYERS:
                global drawer_id

                code = ApplicationCode.GAME_ASSIGN_ROLE
                players_dict = {}

                # Initalize the client list
                for cur_user in active_users:
                    players_dict[cur_user.get_username()] = '0'

                # Role assignment
                if active_users.index(user) == 0:
                    drawer_id = random.randint(0, len(active_users) - 1)

                if active_users.index(user) == drawer_id:
                    reply_msg = json.dumps(
                        {'code': code, 'role': Role.Drawer})
                else:
                    reply_msg = json.dumps(
                        {'code': code, 'role': Role.Guesser, 'players_dict': players_dict})
            else:
                reply_msg = json.dumps(
                    {'code': ApplicationCode.CONTINUE_WAITING})
                if active_users.index(user) == 0:
                    start_new_thread(countdown, (timer,))

            send_reply_msg(user, reply_msg)
            #

        # LOGOUT
        if received_msg['code'] == ApplicationCode.LOGOUT:
            logout(user)


def login_authenticate(user: User, username: str, password: str):
    # check if given username and password is in the database

    # Arguments:
    # -- username: username inputed by user
    # -- password: password inputed by user

    global UsersDatabase
    if username not in UsersDatabase.keys() or password != UsersDatabase[username]['password']:
        print("Username or password is incorrect")
        return ApplicationCode.LOGIN_ERR_INCORRECT

    if UsersDatabase[username]['logged-in']:
        print("User has already logged in")
        return ApplicationCode.LOGIN_ERR_ALREADY_LOGGED_IN

    UsersDatabase[username]['logged-in'] = True
    user.set_username(username)
    return ApplicationCode.LOGIN_SUCCESS


def logout(user: User):
    # un-register user

    # Arguments:
    # -- user: an user initiating logout

    print("Goodbye, ", user.get_connection().getpeername())
    if user.get_username() is not None:
        UsersDatabase[user.get_username()]['logged-in'] = False
    active_users.remove(user)


def countdown(timer: Timer):
    # wait for timer to finish counting down, then destroy thread

    # Arguments:
    # -- timer: timer object init before creating the thread

    # Returns:
    # True, which destroy the thread

    timer.start_countdown()
    return True


def send_reply_msg(user: User, message: str):
    # Sends the reply message to client

    # Arguments:
    # -- user: the recipient client's user object
    # -- message: the message to be sent

    print('Reply message sent to',
          user.get_connection().getpeername(), ':', message)
    user.get_connection().sendall(str.encode(message))


def main():
    # Load user database
    with open('./users.csv') as f:
        reader = csv.DictReader(f)

        global UsersDatabase
        UsersDatabase = {row['Username']: {'password': row['Password'],
                                           'logged-in': False} for row in reader}
        f.close()

    # load word database
    with open("./word_list.txt", "r") as f:
        global Word_list
        for line in f:
            stripped_line = line.strip()
            Word_list.append(stripped_line)

        f.close()

    HOST = "127.0.0.1"
    PORT = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    s.settimeout(1.0)

    # only listens for a maximum of MAX_PLAYER connections
    s.listen(MAX_PLAYERS)
    print("Socket is listening on port", PORT)

    while True:
        try:
            # Establish a connection with a client
            connection, addr = s.accept()
            newUser = User(connection)
            active_users.append(newUser)

            print("Connected to: ", addr[0], ':', addr[1])

            # Start a nwe thread and return its identifier
            start_new_thread(handle_request, (newUser,))
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            for user in active_users:
                user.get_connection().close()
            break

    s.close()


if __name__ == "__main__":
    main()

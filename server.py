from classes.Users import User
from classes.enums.ApplicationCode import ApplicationCode
from classes.enums.Role import Role
from classes.enums.SystemConst import SystemConst

from classes.Server.Clock import Clock
from classes.Server.GameLogic import GameLogic

import socket
import csv
import json
import math
from random import randint
import time

from threading import Timer
from _thread import start_new_thread

UsersDatabase = {}  # Database of users and passwords information

clock = None

active_users = []  # A list of currently active users
gameLogic = None

# num_of_packages = 0  # TODO: reset every round
# package_wait_timeout_started = False  # TODO: reset every round
# broadcast_request_sent = False  # TODO: reset every round
# image_pkgs = []  # TODO: reset every round


def handle_request(user: User):
    # A thread serving each client

    # Arguments:
    # -- user: the client's user object

    while True:
        data = user.get_connection().recv(SystemConst.MESSAGE_SIZE)

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
            # if active_users.index(user) <= SystemConst.MAX_PLAYERS:
            #     reply_msg = json.dumps(
            #         {'code': ApplicationCode.JOIN_ROOM_SUCCESS, 'cur_time': clock.get_curtime()})
            # else:
            #     reply_msg = json.dumps({'code': ApplicationCode.JOIN_ROOM_ERR})
        #

        # WAIT TIME REQUEST
        if received_msg['code'] == ApplicationCode.WAIT_TIME_REQUEST:
            global clock

            print(f"user's index: {active_users.index(user)}")
            if active_users.index(user) == 0:
                clock = Clock(SystemConst.WAITING_FOR_PLAYERS)
                clock.start_countdown()

            # Reply with the current time
            reply_msg = json.dumps(
                {'code': ApplicationCode.START_WAITING,
                    'current_time': round(clock.get_curtime(), 2)})
            send_reply_msg(user, reply_msg)

        #

         # GAME START REQUEST
        if received_msg['code'] == ApplicationCode.GAME_START_REQUEST:
            num_of_users = len(active_users)

            if num_of_users >= SystemConst.MIN_PLAYERS and num_of_users <= SystemConst.MAX_PLAYERS:
                # Initalize the player dictionary
                usernames = [user.get_username() for user in active_users]
                players_dict = gameLogic.create_players_dict(usernames)

                # Role assignment and game logic instatiation
                if not gameLogic.if_drawer_appointed():
                    drawer_id = gameLogic.appoint_drawer()
                    print(f"Drawer's index: {drawer_id}")
                    gameLogic.set_drawer_name(
                        active_users[drawer_id].get_username())

                # Create the reply message
                reply_json = {}
                reply_json['code'] = ApplicationCode.GAME_ASSIGN_ROLE

                if active_users.index(user) == gameLogic.get_drawer_id():
                    # The player is selected as a drawer
                    reply_json['role'] = Role.Drawer
                    keyword = gameLogic.generate_keyword()
                    reply_json['keyword'] = keyword
                else:
                    # The player is selected as a guesser

                    # make sure a keyword is selected
                    while True:
                        if gameLogic.get_keyword() != '':
                            break

                    reply_json['role'] = Role.Guesser
                    reply_json['players_dict'] = players_dict
                    reply_json['drawer_name'] = active_users[gameLogic.get_drawer_id(
                    )].get_username()
                    reply_json['obc_keyword'] = gameLogic.generate_obscurd_keyword()

                reply_msg = json.dumps(reply_json)
                # Stop the clock
                clock.stop_clock()
                ##

            else:
                reply_msg = json.dumps(
                    {'code': ApplicationCode.CONTINUE_WAITING})

            send_reply_msg(user, reply_msg)
            #

        # RECEIVE IMAGE SEND REQUEST
        if received_msg['code'] == ApplicationCode.SEND_IMAGE_REQUEST:
            gameLogic.set_total_num_of_pkgs(received_msg['num_pkgs'])
            gameLogic.set_drawer_time_left(received_msg['time_left'])
            reply_msg = json.dumps(
                {'code': ApplicationCode.READY_TO_RECEIVE_IMAGE})
            send_reply_msg(user, reply_msg)
        #

        # RECEIVE IMAGE AND SENT BROADCAST REQUEST TO GUESSERS
        if received_msg['code'] == ApplicationCode.SEND_IMAGE:
            # image_pkgs.append(received_msg['image'])
            gameLogic.append_image_pkg(received_msg['image'])
            print("package received")

            if gameLogic.if_all_image_pkgs_received() and not gameLogic.if_broadcast_request_sent():
                print("All packages received")
                total_num_pkgs = gameLogic.get_total_num_of_pkgs()

                for usr in active_users:
                    if active_users.index(usr) != gameLogic.get_drawer_id():
                        reply_msg = json.dumps(
                            {'code': ApplicationCode.BROADCASE_IMAGE_REQUEST,
                             'num_pkgs': total_num_pkgs})
                        send_reply_msg(usr, reply_msg)
                    else:
                        reply_msg = json.dumps({
                            'code': ApplicationCode.IMAGE_RECEIVED,
                            'role': Role.Guesser,
                            'players_dict': gameLogic.get_players_dict()
                        })
                        send_reply_msg(usr, reply_msg)

                gameLogic.broadcast_request_sent()

            # Set a timeout to wait for all packages to be sent
            if not gameLogic.if_package_wait_timeout_started():
                timer = Timer(SystemConst.WAIT_IMAGE_TIMEOUT,
                              image_send_checkup, (user, ))
                timer.start()
                gameLogic.package_wait_timeout_started()

        if received_msg['code'] == ApplicationCode.READY_TO_BROADCAST_IMAGE:
            broadcast_image(user)

        if received_msg['code'] == ApplicationCode.BROADCAST_IMAGE_PACKAGES_LOSS:
            broadcast_image(user)
        #

        # BROADCAST GUESSER MESSAGE
        if received_msg['code'] == ApplicationCode.SEND_ANSWER:
            gameLogic.set_guesser_time_left(received_msg['time_left'])
            reply_json = received_msg

            reply_json['code'] = ApplicationCode.BROADCAST_ANSWER

            reply_msg = json.dumps(reply_json)

            for usr in active_users:
                if usr.get_username() != reply_json['username']:
                    send_reply_msg(usr, reply_msg)

            print("Message broadcasted")

            # Check if answer contains the keyword
            answer = reply_json['message']
            if gameLogic.check_answer(answer):
                scores_earned = gameLogic.calculate_score_earned()
                drawer_score_earned = scores_earned['drawer']
                guesser_score_earned = scores_earned['guesser']

                gameLogic.add_player_score(
                    gameLogic.get_drawer_name(), drawer_score_earned)
                gameLogic.add_player_score(
                    user.get_username(), guesser_score_earned)

                reply_msg = json.dumps({'code': ApplicationCode.RIGHT_GUESS_FOUND,
                                        'keyword': gameLogic.get_keyword(),
                                        'right_guesser': user.get_username(),
                                        'scores_earned': scores_earned,
                                        'players_dict': gameLogic.get_players_dict()})
                for usr in active_users:
                    send_reply_msg(usr, reply_msg)

                # Reset round
        #         gameLogic.reset_round()
        #         drawer_id = gameLogic.appoint_drawer()
        #         print(f"Drawer's index: {drawer_id}")
        #         gameLogic.set_drawer_name(
        #             active_users[drawer_id].get_username())

        #         # Drawer's reply message
        #         reply_msg = json.dumps({'code': ApplicationCode.GAME_ASSIGN_ROLE,
        #                                 'role': Role.Drawer,
        #                                'keyword': gameLogic.generate_keyword()})
        #         send_reply_msg(active_users[drawer_id], reply_msg)
        #         #

        #         # Guesser's reply message
        #         reply_msg = json.dumps({'code': ApplicationCode.GAME_ASSIGN_ROLE,
        #                                 'role': Role.Guesser,
        #                                 'players_dict': gameLogic.get_players_dict(),
        #                                 'drawer_name': active_users[drawer_id].get_username(),
        #                                 'obc_keyword': gameLogic.generate_obscurd_keyword()})
        #         for usr in active_users:
        #             if active_users.index(usr) != drawer_id:
        #                 send_reply_msg(usr, reply_msg)
        # #

        # GIVE HINT
        if received_msg['code'] == ApplicationCode.REQUEST_HINT:
            hinted_keyword = gameLogic.get_hinted_keyword()

            reply_msg = json.dumps({'code': ApplicationCode.GIVE_HINT,
                                    'hinted_keyword': hinted_keyword})
            send_reply_msg(user, reply_msg)
        #

        if received_msg['code'] == ApplicationCode.GUESSER_TIME_OUT:
            reply_msg = json.dumps(
                {'code': ApplicationCode.TIME_OUT_ROUND_END,
                 'keyword': gameLogic.get_keyword()})
            if not gameLogic.if_time_out_replied():
                gameLogic.timeout_replied()
                for usr in active_users:
                    send_reply_msg(usr, reply_msg)

        # LOGOUT
        if received_msg['code'] == ApplicationCode.LOGOUT:
            logout(user)
        #


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
    active_users.append(user)
    return ApplicationCode.LOGIN_SUCCESS


def image_send_checkup(user):
    # Check if all image packages have been received, send a failure message if not

    if not gameLogic.if_all_image_pkgs_received():
        reply_msg = json.dumps(
            {'code': ApplicationCode.IMAGE_PACKAGES_LOSS})
        send_reply_msg(user, reply_msg)


def broadcast_image(user):
    image_pkgs = gameLogic.get_image_pkg()

    for package in image_pkgs:
        reply_msg = json.dumps({
            'code': ApplicationCode.BROADCAST_IMAGE,
            'image': package
        })
        send_reply_msg(user, reply_msg)
        print("payload packed")


def logout(user: User):
    # un-register user

    # Arguments:
    # -- user: an user initiating logout

    print("Goodbye, ", user.get_connection().getpeername())
    if user.get_username() is not None:
        UsersDatabase[user.get_username()]['logged-in'] = False
    active_users.remove(user)

    print(f'number of active users: {len(active_users)}')

    if len(active_users) == 0:
        clock.stop_clock()


def send_reply_msg(user: User, message: str):
    # Sends the reply message to client

    # Arguments:
    # -- user: the recipient client's user object
    # -- message: the message to be sent

    print('Reply message sent to',
          user.get_connection().getpeername(), ':', message)
    user.get_connection().send(str.encode(message))
    time.sleep(SystemConst.TIME_BETWEEN_REQUEST)


def main():
    # Load user database
    with open('./users.csv') as f:
        reader = csv.DictReader(f)

        global UsersDatabase
        UsersDatabase = {row['Username']: {'password': row['Password'],
                                           'logged-in': False} for row in reader}
        f.close()

    HOST = SystemConst.HOST
    PORT = SystemConst.PORT

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    s.settimeout(1.0)

    # only listens for a maximum of MAX_PLAYER connections
    s.listen(SystemConst.MAX_PLAYERS)
    print("Socket is listening on port", PORT)

    global gameLogic
    gameLogic = GameLogic()

    while True:
        try:
            # Establish a connection with a client
            connection, addr = s.accept()
            newUser = User(connection)

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

import socket
import csv
import json

from _thread import *
import threading

MAX_PLAYERS = 5
players = []
users = {}

# Application codes
LOGIN_SUCCESS = '100'
LOGIN_ERR_INCORRECT = '101'
LOGIN_ERR_ALREADY_LOGGED_IN = '102'


def handle_request(c):
    while True:
        data = c.recv(2048)

        if not data:
            print("Goodbye")
            players.remove(c)
            break

        received_msg = data.decode('utf-8')
        received_msg = json.loads(received_msg)

        if received_msg['code'] == '10':
            return_code = login_authenticator(
                received_msg['username'], received_msg['password'])

            reply_msg = json.dumps({'code': return_code})
            print(reply_msg)

        #  if received_msg['code'] == '20':
        # TODO

        c.sendall(str.encode(reply_msg))


def login_authenticator(username, password):
    global users
    if username not in users.keys() or password != users[username]['password']:
        print("Username or password is incorrect")
        return LOGIN_ERR_INCORRECT

    if users[username]['logged-in']:
        print("User has already logged in")
        return LOGIN_ERR_ALREADY_LOGGED_IN

    users[username]['logged-in'] = True
    return LOGIN_SUCCESS


def main():
    HOST = "127.0.0.1"
    PORT = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    s.listen(MAX_PLAYERS)
    print("Socket is listening on port", PORT)

    # get list of users
    with open('./users.csv') as f:
        reader = csv.DictReader(f)

        global users
        users = {row['Username']: {'password': row['Password'],
                                   'logged-in': False} for row in reader}

    # print(users)

    while True:
        # Establish a connection with a client
        c, addr = s.accept()
        players.append(c)

        print("Connected to: ", addr[0], ':', addr[1])

        # Start a nwe thread and return its identifier
        start_new_thread(handle_request, (c,))

    s.close()


if __name__ == "__main__":
    main()

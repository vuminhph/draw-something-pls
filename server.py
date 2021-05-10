import socket
import csv
import json

from _thread import *
import threading

MAX_PLAYERS = 5
players = []
users = {}

# Application codes
SUCCESS = '101'
NO_USRNAME = '102'
WRONG_PASSWD = '103'


def worker_thread(c):
    while True:
        data = c.recv(2048)

        if not data:
            print("Goodbye")
            players.remove(c)
            break

        received_msg = data.decode('utf-8')
        received_msg = json.loads(received_msg)

        if received_msg['code'] == '100':
            return_code = login_authenticator(
                received_msg['username'], received_msg['password'])
            reply_msg = json.dumps({'code': return_code})

        print(reply_msg)

        c.sendall(str.encode(reply_msg))


def login_authenticator(username, password):
    global users
    if username not in users.keys():
        return NO_USRNAME
    if password != users[username]:
        return WRONG_PASSWD
    return SUCCESS


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
        users = {row['Username']: row['Password'] for row in reader}

    # print(users)

    while True:
        # Establish a connection with a client
        c, addr = s.accept()
        players.append(c)

        print("Connected to: ", addr[0], ':', addr[1])

        # Start a nwe thread and return its identifier
        start_new_thread(worker_thread, (c,))

    s.close()


if __name__ == "__main__":
    main()

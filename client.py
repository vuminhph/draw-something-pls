import socket
import json

HOST = '127.0.0.1'
PORT = 5555


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    username = 'iphy'
    password = 'pwd3'

    send_msg = json.dumps(
        {'code': '100', 'username': username, 'password': password})

    print("Login in as", username, "\nPassword: ", password)
    s.send(str.encode(send_msg))

    reply_msg = s.recv(2048)
    reply_msg = json.loads(reply_msg.decode('utf-8'))

    if reply_msg['code'] == '101':
        print("Login successfully!")


if __name__ == "__main__":
    main()

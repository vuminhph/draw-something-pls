from Client.GUI import GUI


def main():
    HOST = '127.0.0.1'
    PORT = 5555

    game = GUI(host=HOST, port=PORT)


if __name__ == "__main__":
    main()

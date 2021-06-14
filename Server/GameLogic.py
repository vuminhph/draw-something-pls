
class GameLogic():
    def __init__(self):
        # load word database
        with open("./word_list.txt", "r") as f:
            self.__word_list = []

            for line in f:
                self.__word_list.append(line.strip())

            f.close()

        print(self.__word_list[0])
        print('ok')

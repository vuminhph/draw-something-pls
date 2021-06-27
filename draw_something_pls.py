from classes.Client.GUI import GUI
from classes.enums.SystemConst import SystemConst


def main():
    game = GUI(host=SystemConst.HOST, port=SystemConst.PORT)


if __name__ == "__main__":
    main()

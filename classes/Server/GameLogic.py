from classes.enums.SystemConst import SystemConst

import random
from random import randint
from math import ceil


class GameLogic():
    def __init__(self):
        # load word database
        with open("./word_list.txt", "r") as f:
            self.__word_list = []

            for line in f:
                self.__word_list.append(line.strip())

            f.close()

        self.__is_drawer_appointed = False
        self.__appointed_drawer_id = []

        self.__keyword = ''
        self.__is_hint_given = False
        self.__hinted_keyword = ''

        self.__total_num_of_pkgs = 0  # TODO: reset every round
        self.__is_package_wait_timeout_started = False  # TODO: reset every round
        self.__is_broadcast_request_sent = False  # TODO: reset every round
        self.__image_pkgs = []  # TODO: reset every round

    def if_drawer_appointed(self):
        return self.__is_drawer_appointed

    def appoint_drawer(self):
        # Returns: the appointed drawer id
        num_of_players = len(self.__players_dict)
        self.__drawer_id = random.choice([id for id in range(
            num_of_players - 1) if id not in self.__appointed_drawer_id])

        self.__is_drawer_appointed = True
        self.__appointed_drawer_id.append(self.__drawer_id)
        return self.__drawer_id

    def get_drawer_id(self):
        return self.__drawer_id

    def set_drawer_name(self, drawer_name):
        self.__drawer_name = drawer_name

    def get_drawer_name(self):
        return self.__drawer_name

    def create_players_dict(self, usernames):
        self.__players_dict = {}
        for username in usernames:
            self.__players_dict[username] = str(0)
        return self.__players_dict

    def get_players_dict(self):
        return self.__players_dict

    def calculate_score_earned(self):
        scores_earned = {}
        scores_earned['drawer'] = self.__drawer_time_left * \
            SystemConst.DRAWER_SCORE_MULTI
        scores_earned['guesser'] = self.__guesser_time_left * \
            SystemConst.GUESSER_SCORE_MULTI

        return scores_earned

    def add_player_score(self, username: str, score: int):
        self.__players_dict[username] = str(
            int(self.__players_dict[username]) + score)
        self.__players_dict = {k: v for k, v in sorted(
            self.__players_dict.items(), key=lambda item: int(item[1]), reverse=True)}

    def generate_keyword(self):
        index = random.randint(0, len(self.__word_list) - 1)
        self.__keyword = self.__word_list[index].upper()
        return self.__keyword

    def get_keyword(self):
        return self.__keyword

    def get_hinted_keyword(self):
        if not self.__is_hint_given:
            self.__hinted_keyword = self.generate_hinted_keyword()
            self.__is_hint_given = True
            return self.__hinted_keyword
        else:
            return self.__hinted_keyword

    def generate_hinted_keyword(self):
        # Generate keyword hint
        # Returns the generated hinted keyword
        num_hint_chars = ceil(len(self.__keyword) *
                              SystemConst.HINT_PERCENTAGE)

        hint_indexes = []
        keyword_indexes = list(range(len(self.__keyword)))
        for i in range(num_hint_chars):
            hint_idx = keyword_indexes[randint(
                0, len(keyword_indexes) - 1)]

            hint_indexes.append(hint_idx)
            keyword_indexes.remove(hint_idx)

        hinted_keyword = ''
        for i in range(len(self.__keyword)):
            if i in hint_indexes:
                hinted_keyword += self.__keyword[i] + ' '
            else:
                hinted_keyword += '_ '

        print("Hinted keyword: ", hinted_keyword)
        self.__hinted_keyword = hinted_keyword

        return self.__hinted_keyword

    def check_answer(self, answer):
        if self.__keyword in answer.upper():
            print("Right answer found!")
            return True
        else:
            return False

    def generate_obscurd_keyword(self):
        obc_keyword = ''
        for c in self.__keyword:
            if c == ' ':
                obc_keyword += c
            else:
                obc_keyword += '_ '

        return obc_keyword

    def set_drawer_time_left(self, time_left):
        self.__drawer_time_left = time_left

    def set_guesser_time_left(self, time_left):
        self.__guesser_time_left = time_left

    def reset_round(self):
        self.__is_drawer_appointed = False

        self.__keyword = ''
        self.__is_hint_given = False
        self.__hinted_keyword = ''

        self.__is_package_wait_timeout_started = False
        self.__is_broadcast_request_sent = False
        self.__image_pkgs = []

    # IMAGE SENDING LOGIC
    def append_image_pkg(self, package):
        self.__image_pkgs.append(package)

    def get_image_pkg(self):
        return self.__image_pkgs

    def get_num_of_pkgs(self):
        return len(self.__image_pkgs)

    def get_total_num_of_pkgs(self):
        return self.__total_num_of_pkgs

    def set_total_num_of_pkgs(self, num_pkgs):
        self.__total_num_of_pkgs = num_pkgs

    def if_broadcast_request_sent(self):
        return self.__is_broadcast_request_sent

    def broadcast_request_sent(self):
        self.__is_broadcast_request_sent = True

    def if_package_wait_timeout_started(self):
        return self.__is_package_wait_timeout_started

    def package_wait_timeout_started(self):
        self.__is_package_wait_timeout_started = True

    def if_all_image_pkgs_received(self):
        num_pkgs_received = len(self.__image_pkgs)
        print("number of packages received: ", num_pkgs_received)

        return num_pkgs_received == self.__total_num_of_pkgs
    #

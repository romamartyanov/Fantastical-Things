from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.cardlist import CardList
from scrumban_board_python.scrumban_board.terminal_colors import Colors
# from scrumban_board_python.scrumban_board.calendar import Calendar


class Board:
    def __init__(self, title: str, users_login: deque,
                 description: str = None, cardlists=None):

        self.title = title
        self.description = self.title

        if description is not None:
            self.description = description

        self.cardlists = deque()

        if cardlists is not None:
            if isinstance(cardlists, CardList):
                self.cardlists.append(cardlists)

            elif isinstance(cardlists, deque):
                for cardlist in cardlists:
                    if isinstance(cardlist, CardList):
                        self.cardlists.append(cardlist)
        else:

            to_do = CardList("To-Do")
            doing = CardList("Doing")
            done = CardList("Done")
            overdue = CardList("Overdue")

            self.cardlists.append(to_do)
            self.cardlists.append(doing)
            self.cardlists.append(done)
            self.cardlists.append(overdue)

        self.users_login = deque()
        if isinstance(users_login, str):
            self.users_login.append(users_login)

        elif isinstance(users_login, deque):
            for user_id in users_login:
                if isinstance(user_id, str):
                    self.users_login.append(user_id)

        # self.calendar = Calendar(self.users_id)

        self.id = sha1(("Board: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8')).hexdigest()

    def __str__(self):
        users_id = [user_id for user_id in self.users_login]
        cardlists = [cardlist for cardlist in self.cardlists]

        output = Colors.cardlist_green + """
--- Board ---
Title: {}
Description: {}
ID: {}

Users ID:
{}

Cardlists:
{}

--End Board--
""".format(self.title,
           self.description,
           self.id,
           users_id,
           cardlists) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id for user_id in self.users_login]
        cardlists = [cardlist for cardlist in self.cardlists]

        output = Colors.cardlist_green + """
--- Board ---
Title: {}
Description: {}
ID: {}

Users ID:
{}

Cardlists:
{}

--End Board--
""".format(self.title,
           self.description,
           self.id,
           users_id,
           cardlists) + Colors.end_color

        return output

    def update_board(self, title: str = None, users: deque = None, description: str = None, cardlists: deque = None):
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if cardlists is not None:
            self.cardlists.clear()

            if isinstance(cardlists, CardList):
                self.cardlists.append(cardlists)

            elif isinstance(cardlists, deque):
                for cardlist in cardlists:
                    if isinstance(cardlist, CardList):
                        self.cardlists.append(cardlist)

        if users is not None:
            self.users_login.clear()

            for user in users:
                self.users_login.append(user)

    def find_cardlist(self, cardlist_id=None, title=None):
        if cardlist_id is not None:
            try:
                return next(cardlist for cardlist in self.cardlists if cardlist.id == cardlist_id)
            except StopIteration:
                return None

        elif title is not None:
            try:
                return next(cardlist for cardlist in self.cardlists if cardlist.title == title)
            except StopIteration:
                return None
        else:
            return None

    def add_cardlist(self, new_cardlist: CardList):
        duplicate_cardlist = self.find_cardlist(new_cardlist)

        if duplicate_cardlist is None:
            self.cardlists.append(new_cardlist)

    def remove_cardlist(self, cardlist: CardList = None, cardlist_id: str = None):
        if cardlist is not None:
            duplicate_cardlist = self.find_cardlist(cardlist.id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

        elif cardlist_id is not None:
            duplicate_cardlist = self.find_cardlist(cardlist_id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

    def change_cardlist_position(self, position: int, cardlist: CardList = None, cardlist_id: str = None):
        if cardlist is not None:
            duplicate_cardlist = self.find_cardlist(cardlist.id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

                real_position = position - 1
                self.cardlists.insert(real_position, duplicate_cardlist)

        elif cardlist_id is not None:
            duplicate_cardlist = self.find_cardlist(cardlist_id)

            if duplicate_cardlist is not None:
                self.cardlists.remove(duplicate_cardlist)

                real_position = position - 1
                self.cardlists.insert(real_position, duplicate_cardlist)

    def move_card(self, card_id: str, old_cardlist_id: str, new_cardlist_id: str):
        # for old_cardlist in self.cardlists:
        #     if old_cardlist.id == old_cardlist_id:
        #
        #         for new_cardlist in self.cardlists:
        #             if new_cardlist.id == new_cardlist_id:
        #
        #                 card = old_cardlist.find_card(card_id=card_id)
        #                 old_cardlist.remove_card(card=card)
        #                 new_cardlist.add_card(card)

        old_cardlist = self.find_cardlist(old_cardlist_id)
        new_cardlist = self.find_cardlist(new_cardlist_id)

        card = old_cardlist.find_card(card_id=card_id)
        old_cardlist.remove_card(card=card)
        new_cardlist.add_card(card)



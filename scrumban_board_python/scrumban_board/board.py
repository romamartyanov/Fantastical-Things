from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.cardlist import CardList
from scrumban_board_python.scrumban_board.terminal_colors import Colors
# from scrumban_board_python.scrumban_board.calendar import Calendar


class Board:
    def __init__(self, title: str, users_id: deque,
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

        self.users_id = deque()
        if isinstance(users_id, str):
            self.users_id.append(users_id)

        elif isinstance(users_id, deque):
            for user_id in users_id:
                if isinstance(user_id, str):
                    self.users_id.append(user_id)

        # self.calendar = Calendar(self.users_id)

        self.id = sha1(("Board: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        users_id = [user_id.hexdigest() for user_id in self.users_id]

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
           self.id.hexdigit(),
           users_id,
           self.cardlists) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id.hexdigest() for user_id in self.users_id]

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
           self.id.hexdigit(),
           users_id,
           self.cardlists) + Colors.end_color

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
            self.users_id.clear()

            for user in users:
                self.users_id.append(user)

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

from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.cardlist import CardList
from scrumban_board_python.scrumban_board.user import User


class Board:
    def __init__(self, title: str, users: list, description: str = None, cardlists: list = None):
        self.title = title
        self.description = self.title

        if description is not None:
            self.description = description

        self.cardlists = list()
        for cardlist in cardlists:
            if isinstance(cardlist, CardList):
                self.cardlists.append(cardlist)

        self.users = list()
        for user in users:
            if isinstance(user, User):
                self.cardlists.append(user)

        self.id = sha1(("Board: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def update_board(self, title: str = None, users: list = None, description: str = None, cardlists: list = None):
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if cardlists is not None:
            self.cardlists.clear()

            for cardlist in cardlists:
                if isinstance(cardlist, CardList):
                    self.cardlists.append(cardlist)

        if users is not None:
            self.users.clear()

            for user in users:
                if isinstance(user, User):
                    self.users.append(user)

    def find_cardlist(self, cardlist_id=None, title=None):
        if cardlist_id is not None:
            return next(cardlist for cardlist in self.cardlists if cardlist.id == cardlist_id)

        elif title is not None:
            return next(cardlist for cardlist in self.cardlists if cardlist.title == title)

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

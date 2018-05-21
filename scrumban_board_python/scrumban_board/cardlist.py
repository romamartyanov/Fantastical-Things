from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.card import Card
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class CardList:
    def __init__(self, title: str, cards: deque = None, description: str = None):
        self.title = title
        self.description = description

        self.cards = deque()
        if cards is not None:
            for card in cards:
                if isinstance(card, Card):
                    cards.append(card)

        self.id = sha1(("CardList: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        output = Colors.cardlist_green + """
--- Cardlist ---
Title: {}
Description: {}
ID: {}

Cards: 
{}

---End Cardlist--
""".format(self.title,
           self.description,
           self.id.hexdigest(),
           self.cards) + Colors.ENDC

        return output

    def __repr__(self):
        output = Colors.cardlist_green + """
--- Cardlist ---
Title: {}
Description: {}
ID: {}

Cards: 
{}

---End Cardlist--
""".format(self.title,
           self.description,
           self.id.hexdigest(),
           self.cards) + Colors.ENDC

        return output

    def update_cardlist(self, title: str = None, cards: deque = None, description: str = None):
        if title is not None:
            self.title = title

        if cards is not None:
            self.cards.clear()

            for card in cards:
                if isinstance(card, Card):
                    cards.append(card)

        if description is not None:
            self.description = description

    def find_card(self, card_id=None, title=None):
        if card_id is not None:
            try:
                return next(card for card in self.cards if card.id == card_id)
            except StopIteration:
                return None

        elif title is not None:
            try:
                return next(card for card in self.cards if card.title == title)
            except StopIteration:
                return None

        else:
            return None

    def add_card(self, new_card: Card):
        duplicate_card = self.find_card(card_id=new_card.id)

        if duplicate_card is None:
            self.cards.append(new_card)

    def remove_card(self, card: Card = None, card_id=None):
        if card is not None:
            duplicate_card = self.find_card(card_id=card.id)

            if duplicate_card is not None:
                self.cards.remove(card)

        elif card_id is not None:
            duplicate_card = self.find_card(card_id=card_id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

    def change_card_position(self, position: int, card: Card = None, card_id=None):
        if card is not None:
            duplicate_card = self.find_card(card_id=card.id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

                real_position = position - 1
                self.cards.insert(real_position, duplicate_card)

        elif card_id is not None:
            duplicate_card = self.find_card(card_id=card_id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

                real_position = position - 1
                self.cards.insert(real_position, duplicate_card)

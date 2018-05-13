from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.card import Card


class CardList:
    def __init__(self, title: str, cards: list, description: str = None):
        self.title = title
        self.description = description

        self.cards = list()
        for card in cards:
            if isinstance(card, Card):
                cards.append(card)

        self.id = sha1(("CardList: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def find_card(self, card_id=None, title=None):
        if card_id is not None:
            return next(card for card in self.cards if card.id == card_id)

        elif title is not None:
            return next(card for card in self.cards if card.title == title)

    def add_card(self, new_card: Card):
        duplicate_card = self.find_card(card_id=new_card.id)

        if duplicate_card is None:
            self.cards.append(new_card)

    def remove_card(self, card: Card = None, card_id=None):
        if card is not None:
            remove_card = self.find_card(card_id=card.id)

            if remove_card is not None:
                self.cards.remove(card)

        elif card_id is not None:
            remove_card = self.find_card(card_id=card_id)

            if remove_card is not None:
                self.cards.remove(remove_card)

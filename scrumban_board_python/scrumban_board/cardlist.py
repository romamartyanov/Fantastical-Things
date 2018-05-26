from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.card import Card
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class CardList:
    """
    Board contains Cardlists with cards

    Example:
    to_do = CardList(self.logger, "To-Do")
    doing = CardList(self.logger, "Doing")
    done = CardList(self.logger, "Done")
    overdue = CardList(self.logger, "Overdue")
    """

    def __init__(self, logger, title: str,
                 cards=None, description: str = None):
        """
        Initialising of Cardlist

        :param logger: client logger
        :param title: cardlist title
        :param cards: deque of cards (or Card)
        :param description: cardlist description
        """
        self.title = title
        self.description = description
        self.logger = logger

        self.cards = deque()
        if cards is not None:
            if isinstance(cards, Card):
                self.cards.append(cards)

            elif isinstance(cards, deque):
                for card in cards:
                    if isinstance(card, Card):
                        cards.append(card)

        self.id = sha1(("CardList: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8')).hexdigest()

        self.logger.info("Cardlist ({}) was created".format(self.id))

    def __str__(self):
        cards = [card for card in self.cards]

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
           self.id,
           cards) + Colors.end_color

        return output

    def __repr__(self):
        cards = [card for card in self.cards]

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
           self.id,
           cards) + Colors.end_color

        return output

    def update_cardlist(self, title: str = None, cards: deque = None, description: str = None):
        """
        Cardlist updating

        :param title: new title
        :param cards: new cards (or Card)
        :param description: new description
        :return:
        """
        if title is not None:
            self.title = title

        if cards is not None:
            self.cards.clear()

            if isinstance(cards, Card):
                self.cards.append(cards)

            elif isinstance(cards, deque):
                for card in cards:
                    if isinstance(card, Card):
                        cards.append(card)

        if description is not None:
            self.description = description

        self.logger.info("Cardlist ({}) was updated".format(self.id))

    def find_card(self, card_id=None, card_title=None):
        """
        Searching card in the cardlist

        :param card_id: сard id
        :param card_title: card title
        :return:
        """
        if card_id is not None:
            try:
                card = next(card for card in self.cards if card.id == card_id)
                self.logger.info("Card ({}) was found by card_id in Cardlist ({})".format(card_id,
                                                                                          self.id))

                return card
            except StopIteration:
                self.logger.info("Card ({}) wasn't found by card_id in Cardlist ({})".format(card_id,
                                                                                             self.id))

        elif card_title is not None:
            try:
                card = next(card for card in self.cards if card.title == card_title)
                self.logger.info("Card ({}) wasn found by card_title in Cardlist ({})".format(card_title,
                                                                                              self.id))
                return card
            except StopIteration:
                self.logger.info("Card ({}) wasn't found by card_title in Cardlist ({})".format(card_title,
                                                                                                self.id))
        return None

    def add_card(self, new_card: Card):
        """
        Addind new card

        :param new_card: new card
        :return:
        """
        duplicate_card = self.find_card(card_id=new_card.id)

        if duplicate_card is None:
            self.cards.append(new_card)

            self.logger.info("Card ({}) was added in Cardlist ({})".format(new_card.id,
                                                                           self.id))

    def remove_card(self, card: Card = None, card_id=None):
        """
        Removing card

        :param card: Card for removing
        :param card_id: card id for removing
        :return:
        """
        if card is not None:
            duplicate_card = self.find_card(card_id=card.id)

            if duplicate_card is not None:
                self.cards.remove(card)

                self.logger.info("Card ({}) was removed from Cardlist ({})".format(duplicate_card.id,
                                                                                   self.id))

        elif card_id is not None:
            duplicate_card = self.find_card(card_id=card_id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

                self.logger.info("Card ({}) was removed from Cardlist ({})".format(duplicate_card.id,
                                                                                   self.id))

    def change_card_position(self, position: int, card: Card = None, card_id: str = None):
        """
        Changing card position in cardlist

        :param position: 1, 2 .. n
        :param card: Card
        :param card_id: card id
        :return:
        """
        if card is not None:
            duplicate_card = self.find_card(card_id=card.id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

                real_position = position - 1
                self.cards.insert(real_position, duplicate_card)

                self.logger.info("Card ({}) was moved in Cardlist ({}) to position {}".format(duplicate_card.id,
                                                                                              self.id,
                                                                                              real_position))

        elif card_id is not None:
            duplicate_card = self.find_card(card_id=card_id)

            if duplicate_card is not None:
                self.cards.remove(duplicate_card)

                real_position = position - 1
                self.cards.insert(real_position, duplicate_card)

                self.logger.info("Card ({}) was moved in Cardlist ({}) to position {}".format(duplicate_card.id,
                                                                                              self.id,
                                                                                              real_position))

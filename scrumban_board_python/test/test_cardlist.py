import unittest

from collections import deque
import test as _test
from scrumban_board import cardlist as _cardlist


class CardlistTest(_test.TestCase):
    def test_get_cards(self):
        card = _cardlist.Card("card", "romamartyanov")
        self.assertEqual(type(_cardlist.CardList.get_cards(card)), deque)

    def test_change_card_position(self):
        raised = False

        card1 = _cardlist.Card("card1", "romamartyanov")
        card2 = _cardlist.Card("card2", "romamartyanov")
        card3 = _cardlist.Card("card3", "romamartyanov")

        cardlist = _cardlist.CardList("title")

        cardlist.add_card(card1)
        cardlist.add_card(card2)
        cardlist.add_card(card3)

        try:
            cardlist.change_card_position(0, card1)
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised')


if __name__ == "__main__":
    unittest.main()

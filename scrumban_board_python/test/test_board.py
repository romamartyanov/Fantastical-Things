import unittest

from collections import deque
import test as _test
from scrumban_board import board as _board
from scrumban_board import Card


class BoardTest(_test.TestCase):
    def test_get_cardlists(self):
        self.assertEqual(type(_board.Board.get_cardlists("cardlist")), deque)
        self.assertEqual(type(_board.Board.get_cardlists(None)), deque)

    def test_get_users_login(self):
        self.assertEqual(type(_board.Board.get_users_login("romamartyanov")), deque)

    def test_move_card(self):
        cardlist1 = _board.CardList("1")
        cardlist2 = _board.CardList("2")

        board = _board.Board("board_1", "romamartyanov")
        board.add_cardlist(cardlist1)
        board.add_cardlist(cardlist2)

        card = Card("task", "romamartyanov")
        cardlist1.add_card(card)

        raised = False
        try:
            board.move_card(card.id, cardlist1.id, cardlist2.id)
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised')


if __name__ == "__main__":
    unittest.main()
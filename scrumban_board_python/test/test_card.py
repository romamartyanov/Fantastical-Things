import unittest

from collections import deque
import test as _test
from scrumban_board import card as _card


class CardTest(_test.TestCase):
    def test___init___(self):
        raised = False
        try:
            card = _card.Card("card", "romamartyanov")
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised')

    def test_get_task(self):
        raised = False
        try:
            _card.Card.get_task("task")
        except Exception:
            raised = True
        self.assertFalse(raised, 'Exception raised')

        self.assertEqual(type(_card.Card.get_task("task")), _card.Task)

    def test_get_users_login(self):
        self.assertEqual(type(_card.Card.get_users_login("login")), deque)

    def test_get_remind_list(self):
        remind = _card.Remind("2018/10/10", "romamartyanov")
        self.assertEqual(type(_card.Card.get_remind_list(remind)), deque)


if __name__ == "__main__":
    unittest.main()
import unittest

from collections import deque
import test as _test
from scrumban_board import user as _user


class TeamTest(_test.TestCase):
    def test_get_team_boards(self):
        self.assertEqual(type(_user.User.get_user_boards(login="romamartyanov")), deque)

        board = _user.Board("board", "romamartyanov")
        self.assertEqual(type(_user.User.get_user_boards(login="romamartyanov", boards=board)), deque)

    def test_get_team_members_login(self):
        self.assertEqual(type(_user.User.get_teams_list(deque("romamartyanov"))), deque)


if __name__ == "__main__":
    unittest.main()

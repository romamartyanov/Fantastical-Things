import unittest

from collections import deque
import test as _test
from scrumban_board import team as _team


class TeamTest(_test.TestCase):
    def test_get_team_boards(self):
        self.assertEqual(type(_team.Team.get_team_boards(login="romamartyanov")), deque)

        board = _team.Board("board", "romamartyanov")
        self.assertEqual(type(_team.Team.get_team_boards(login="romamartyanov", boards=board)), deque)

    def test_get_team_members_login(self):
        self.assertEqual(type(_team.Team.get_team_members_login("romamartyanov")), deque)


if __name__ == "__main__":
    unittest.main()

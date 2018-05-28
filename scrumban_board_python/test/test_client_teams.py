import unittest

from collections import deque
import test as _test
from scrumban_board import client_teams as _client_teams


class ClientTeamsTest(_test.TestCase):

    def test_get_users(self):
        try:
            self.assertRaises(_client_teams.ClientTeams.get_client_teams(deque("romamartyanov")), ValueError)
        except Exception:
            pass

        team = _client_teams.Team("My Team", "my_team, ", "romamartyanov")
        d = deque()
        d.append(team)

        self.assertEqual(type(_client_teams.ClientTeams.get_client_teams(d)), deque)


if __name__ == "__main__":
    unittest.main()

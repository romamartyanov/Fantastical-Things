import unittest

from collections import deque
import test as _test
from scrumban_board import client_users as _client_users


class ClientUsersTest(_test.TestCase):

    def test_get_users(self):
        try:
            self.assertRaises(_client_users.ClientUsers.get_users("romamartyanov"), ValueError)
        except Exception:
            pass

        self.assertEqual(type(_client_users.ClientUsers.get_users(deque("romamartyanov"))), deque)


if __name__ == "__main__":
    unittest.main()

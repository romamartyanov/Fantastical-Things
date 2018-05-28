import unittest


import test as _test
from scrumban_board import subtask as _subtask


class SubtaskTest(_test.TestCase):
    def test_get_id(self):
        subtask = _subtask.Subtask(title="subtask")

        if type(subtask.get_id()) is not str:
            raise ValueError


if __name__ == "__main__":
    unittest.main()

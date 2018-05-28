import unittest

from collections import deque

import test as _test
from scrumban_board import task as _task


class TaskTest(_test.TestCase):
    def test_get_subtask_list(self):
        if type(_task.Task.get_subtask_list(['subtask'])) is not deque:
            raise ValueError

    def test_change_subtask_position(self):
        raised = False

        subtask1 = _task.Subtask("subtask1")
        subtask2 = _task.Subtask("subtask1")
        subtask3 = _task.Subtask("subtask1")

        task = _task.Task("task")
        try:
            task.add_subtask(subtask1)
            task.add_subtask(subtask2)
            task.add_subtask(subtask1)
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised')

        raised = False

        try:
            task.change_subtask_position(0, subtask3)
        except Exception:
            raised = True

        self.assertFalse(raised, 'Exception raised')


if __name__ == "__main__":
    unittest.main()

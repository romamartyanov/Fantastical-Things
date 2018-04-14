from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.subtask import Subtask


class Task:
    def __init__(self, title=None, description=None, subtasks_list=None):
        if title is not None:
            self.title = title
            self.description = title
        else:
            self.title = "Task at " + str(datetime.datetime.now())

        if description is not None:
            self.description = description
        else:
            self.description = "Task at " + str(datetime.datetime.now())

        if subtasks_list is not None:
            if isinstance(subtasks_list, list):
                self.subtasks_list = subtasks_list
        else:
            self.subtasks_list = list()

        self.completed = False

        self.id = sha1(("Task: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def add_subtask(self, subtask=None):
        if subtask is not None:
            if isinstance(subtask, Subtask):
                self.subtasks_list.append(subtask)

            elif isinstance(subtask, str):
                new_subtask = Subtask(title=subtask)
                self.subtasks_list.append(new_subtask)

    def remove_subtask(self, subtask=None, subtask_id=None):
        if subtask is not None:
            self.subtasks_list.remove(subtask)

        elif subtask_id is not None:
            if subtask_id is not None:
                subtask = next(subtask for subtask in self.subtasks_list if subtask.id == subtask_id)
                self.subtasks_list.remove(subtask)

    def find_subtask(self, title=None, subtask_id=None):
        if subtask_id is not None:
            return next(subtask for subtask in self.subtasks_list if subtask.id == subtask_id)

        elif title is not None:
            return next(subtask for subtask in self.subtasks_list if subtask.title == title)

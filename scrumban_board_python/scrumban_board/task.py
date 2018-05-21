from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.subtask import Subtask
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Task:
    def __init__(self, title: str, description: str = None, subtasks_list: deque = None):

        self.title = title
        self.description = title

        if description is not None:
            self.description = description

        self.subtasks_list = deque()
        if subtasks_list is not None:
            for subtask in subtasks_list:
                if isinstance(subtask, Subtask):
                    self.subtasks_list.append(subtask)

        self.completed = False

        self.id = sha1(("Task: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        subtasks_list = [subtask for subtask in self.subtasks_list]

        output = Colors.task_blue + """
--- TASK ---
Title: {}
Description: {}
ID: {}
Completed: {}

Subtasks:
{}

--End Task--
""".format(self.title,
           self.description,
           self.id.hexdigest(),
           self.completed,
           subtasks_list) + Colors.ENDC

        return output

    def update_task(self, title: str = None, description: str = None,
                    subtasks_list: deque = None, completed: bool = None):

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if subtasks_list is not None:
            self.subtasks_list.clear()

            for subtask in subtasks_list:
                if isinstance(subtask, Subtask):
                    self.subtasks_list.append(subtask)

        if completed is not None:
            self.completed = completed

    def find_subtask(self, title: str = None, subtask_id: str = None):
        if subtask_id is not None:
            try:
                return next(subtask for subtask in self.subtasks_list if subtask.id == subtask_id)
            except StopIteration:
                return None

        elif title is not None:
            try:
                return next(subtask for subtask in self.subtasks_list if subtask.title == title)
            except StopIteration:
                return None

        else:
            return None

    def add_subtask(self, subtask: Subtask):
        if isinstance(subtask, Subtask):
            duplicate_subtask = self.find_subtask(title=subtask.title)

            if duplicate_subtask is None:
                self.subtasks_list.append(subtask)

        elif isinstance(subtask, str):
            duplicate_subtask = self.find_subtask(subtask)
            if duplicate_subtask is None:
                duplicate_subtask = Subtask(title=subtask)
                self.subtasks_list.append(duplicate_subtask)

    def remove_subtask(self, subtask: Subtask = None, subtask_id: str = None):
        if subtask is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

        elif subtask_id is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

    def change_subtask_position(self, position: int, subtask: Subtask = None, subtask_id: str = None):
        if subtask is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

                real_position = position - 1
                self.subtasks_list.insert(real_position, duplicate_subtask)

        elif subtask_id is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

                real_position = position - 1
                self.subtasks_list.insert(real_position, duplicate_subtask)

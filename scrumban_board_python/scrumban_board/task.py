import os
import logging.config
import string
import random
import datetime

from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.subtask import Subtask
from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")

class Task:
    """
    Description of Task class

    Example:
    task = scrumban_board.Task("title", "description")
    """

    @staticmethod
    def get_subtask_list(subtasks_list):
        new_subtasks_list = deque()

        if subtasks_list is not None:

            if isinstance(subtasks_list, str):
                subtask = Subtask(subtasks_list)
                new_subtasks_list.append(subtask)

                return new_subtasks_list

            elif isinstance(subtasks_list, deque):
                for subtask in subtasks_list:
                    if isinstance(subtask, Subtask):
                        new_subtasks_list.append(subtask)

                        return new_subtasks_list

        return new_subtasks_list

    def __init__(self, title: str,
                 description: str = None, subtasks_list: deque = None):
        """
        Initialising of task

        :param title: task title
        :param description: task description
        :param subtasks_list: subtasks list
        """

        self.title = title
        self.description = description

        self.subtasks_list = Task.get_subtask_list(subtasks_list)

        self.completed = False

        self.id = self._get_id()

        logger.info("Task ({}) was created".format(self.id))

    def _get_id(self):
        """
        Getting task id with a help of sha1

        :return: sha1 hash
        """

        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.title)))

        return sha1(("Task: " +
                     key + " " +
                     self.title + " " +
                     str(datetime.datetime.now())).encode('utf-8')).hexdigest()

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
           self.id,
           self.completed,
           subtasks_list) + Colors.end_color

        return output

    def update_task(self, title: str = None, description: str = None,
                    subtasks_list=None, completed: bool = None):
        """
        Updating task

        :param title: task title
        :param description: task description
        :param subtasks_list: subtasks list
        :param completed:
        :return:
        """

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if subtasks_list is not None:
            self.subtasks_list = Task.get_subtask_list(subtasks_list)

        if completed is not None:
            self.completed = completed

        logger.info("Task ({}) was updated".format(self.id))

    def find_subtask(self, title: str = None, subtask_id: str = None):
        """
        Searching subtask

        :param title:
        :param subtask_id:
        :return:
        """
        if subtask_id is not None:
            try:
                subtask = next(subtask for subtask in self.subtasks_list if subtask.id == subtask_id)
                logger.info("Subtask ({}) wasn found by subtask_id in Task ({})".format(subtask_id,
                                                                                        self.id))
                return subtask

            except StopIteration:
                logger.info("Subtask ({}) wasn't found by subtask_id in Task ({})".format(subtask_id,
                                                                                          self.id))

        elif title is not None:
            try:
                subtask = next(subtask for subtask in self.subtasks_list if subtask.title == title)
                logger.info("Subtask ({}) wasn found by title in Task ({})".format(title,
                                                                                   self.id))
                return subtask

            except StopIteration:
                logger.info("Subtask ({}) wasn't found by title in Task ({})".format(title,
                                                                                     self.id))
        return None

    def add_subtask(self, subtask):
        """
        Adding new subtask

        :param subtask: Subtask or str
        :return:
        """
        if isinstance(subtask, Subtask):
            duplicate_subtask = self.find_subtask(title=subtask.title)

            if duplicate_subtask is None:
                self.subtasks_list.append(subtask)
                logger.info("Subtask ({}) was added to the Task ({})".format(subtask.id,
                                                                             self.id))

        elif isinstance(subtask, str):
            duplicate_subtask = self.find_subtask(subtask)
            if duplicate_subtask is None:
                new_subtask = Subtask(title=subtask)

                self.subtasks_list.append(new_subtask)
                logger.info("Subtask ({}) was added to the Task ({})".format(new_subtask.id,
                                                                             self.id))

    def remove_subtask(self, subtask: Subtask = None, subtask_id: str = None):
        """
        Removing subtask

        :param subtask: Subtask
        :param subtask_id: subtask id
        :return:
        """
        if subtask is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)
                logger.info("Subtask ({}) was removed from the Task ({})".format(duplicate_subtask.id,
                                                                                 self.id))

        elif subtask_id is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

                logger.info("Subtask ({}) was removed from the Task ({})".format(duplicate_subtask.id,
                                                                                 self.id))

    def change_subtask_position(self, position: int, subtask: Subtask = None, subtask_id: str = None):
        """
        Change Subtask position

        :param position: 1, 2 .. n
        :param subtask: Subtask
        :param subtask_id: subtask id
        :return:
        """
        if subtask is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

                real_position = position - 1
                self.subtasks_list.insert(real_position, duplicate_subtask)

                logger.info("Subtask ({}) was moved in the Task ({}) to position {}".format(duplicate_subtask.id,
                                                                                            self.id,
                                                                                            real_position))

        elif subtask_id is not None:
            duplicate_subtask = self.find_subtask(subtask_id=subtask_id)

            if duplicate_subtask is not None:
                self.subtasks_list.remove(duplicate_subtask)

                real_position = position - 1
                self.subtasks_list.insert(real_position, duplicate_subtask)

                logger.info("Subtask ({}) was moved in the Task ({}) to position {}".format(duplicate_subtask.id,
                                                                                            self.id,
                                                                                            real_position))

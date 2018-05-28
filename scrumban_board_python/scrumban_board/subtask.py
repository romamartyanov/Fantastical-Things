import os
import logging.config
import datetime
import string
import random

from hashlib import sha1

from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Subtask:
    """
    Description of Subtask

    Example:
    task.add_subtask(scrumban_board.Subtask("subtask1"))
    task.add_subtask(scrumban_board.Subtask("subtask2"))
    """

    def __init__(self, title: str,
                 description: str = None):
        """
        Initialising of Subtask

        :param title: subtask title
        :param description: subtask description
        """

        self.title = title
        self.description = description

        self.completed = False

        self.id = self.get_id()

        logger.info("Subtask ({}) was created".format(self.id))

    def __str__(self):
        output = Colors.subtask_lightblue + """
                --- SUBTASK ---
                Title: {}
                Description: {}
                Completed: {}
                ID: {}
                --End Subtask--
""".format(self.title,
           self.description,
           self.completed,
           self.id) + Colors.end_color

        return output

    def __repr__(self):
        output = Colors.subtask_lightblue + """
                --- SUBTASK ---
                Title: {}
                Description: {}
                Completed: {}
                ID: {}
                --End Subtask--
""".format(self.title,
           self.description,
           self.completed,
           self.id) + Colors.end_color

        return output

    def get_id(self):
        """
        Getting subtask id with a help of sha1

        :return: sha1 hash
        """
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.title)))

        return sha1(("Subtask: " +
                     key + " " +
                     self.title + " " +
                     str(datetime.datetime.now())).encode('utf-8')).hexdigest()

    def update_subtask(self, title: str = None, description: str = None, completed: bool = None):
        """
        Updating of Subtask

        :param title: subtask title
        :param description: subtask description        :param description:
        :param completed:
        :return:
        """
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if completed is not None:
            self.completed = completed

        logger.info("Subtask ({}) was updated".format(self.id))

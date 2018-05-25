from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Subtask:
    """
    Description of Subtask

    Example:
    task.add_subtask(scrumban_board.Subtask(client.logger, "subtask1"))
    task.add_subtask(scrumban_board.Subtask(client.logger, "subtask2"))
    """

    def __init__(self, logger, title: str,
                 description: str = None):
        """
        Initialising of Subtask

        :param logger: client logger
        :param title: subtask title
        :param description: subtask description
        """

        self.title = title
        self.description = description
        self.logger = logger

        self.completed = False

        self.id = sha1(("Subtask: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8')).hexdigest()

        self.logger.info("Subtask ({}) was created".format(self.id))

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

        self.logger.info("Subtask ({}) was updated".format(self.id))


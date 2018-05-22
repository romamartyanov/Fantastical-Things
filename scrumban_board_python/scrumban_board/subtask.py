from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Subtask:
    def __init__(self, title: str,
                 description: str = None):

        self.title = title
        self.description = description

        self.completed = False

        self.id = sha1(("Subtask: " + " " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

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
           self.id.hexdigest()) + Colors.end_color

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
           self.id.hexdigest()) + Colors.end_color

        return output

    def update_subtask(self, title: str = None, description: str = None, completed: bool = None):
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if completed is not None:
            self.completed = completed

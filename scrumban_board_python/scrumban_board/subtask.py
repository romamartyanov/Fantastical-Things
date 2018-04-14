from hashlib import sha1
import datetime


class Subtask:
    def __init__(self, title=None, description=None):
        if title is not None:
            self.title = title
            self.description = title
        else:
            self.title = "Subtask at " + str(datetime.datetime.now())

        if description is not None:
            self.description = description
        else:
            self.description = "Subtask at " + str(datetime.datetime.now())

        self.completed = False

        self.id = sha1(("Subtask: " + " " +
                        self.title + " " +
                        self.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

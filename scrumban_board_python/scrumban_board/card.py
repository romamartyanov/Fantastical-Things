from hashlib import sha1
import datetime

from scrumban_board_python.scrumban_board.task import Task
from scrumban_board_python.scrumban_board.remind import Remind
from scrumban_board_python.scrumban_board.user import User


class Card:
    def __init__(self, task=None, reminds_list=None, deadline=None, repeatable_remind=None, users=None):
        if task is not None:
            if isinstance(task, Task):
                self.task = task
        else:
            self.task = Task(title="Task at {}".format(str(datetime.datetime.now())))

        self.reminds_list = list()
        if reminds_list is not None:
            if isinstance(reminds_list, list):
                for remind in reminds_list:
                    if isinstance(remind, Remind):
                        self.reminds_list.append(remind)

            elif isinstance(reminds_list, Remind):
                self.reminds_list.append(reminds_list)

        if deadline is not None:
            if isinstance(deadline, datetime.datetime):
                self.deadline = deadline
            elif isinstance(deadline, str):
                pass
        else:
            self.deadline = None

        if repeatable_remind is not None:
            if isinstance(repeatable_remind, datetime.timedelta):
                self.repeatable_remind = repeatable_remind

            elif isinstance(repeatable_remind, str):
                pass
        else:
            self.repeatable_remind = None

        self.users = list()
        if users is not None:
            if isinstance(users, User):
                self.users.append(users)

            elif isinstance(users, list):
                for user in users:
                    if isinstance(user, User):
                        self.add_remind(user)

        self.id = sha1(("Card: " + " " +
                        self.task.title + " " +
                        self.task.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def add_remind(self, remind):
        if isinstance(remind, Remind):
            self.reminds_list.append(remind)

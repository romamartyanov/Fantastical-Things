from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.task import Task
from scrumban_board_python.scrumban_board.remind import Remind
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Card:
    def __init__(self, task, users_login,
                 reminds_list=None, deadline: Remind = None):

        if isinstance(task, Task):
            self.task = task

        elif isinstance(task, str):
            task = Task(title=task)
            self.task = task

        self.users_login = deque()
        if isinstance(users_login, deque):
            self.users_login = users_login
        elif isinstance(users_login, str):
            self.users_login = deque()
            self.users_login.append(users_login)

        self.reminds_list = deque()
        if reminds_list is not None:
            if isinstance(reminds_list, Remind):
                self.reminds_list.append(reminds_list)

            elif isinstance(reminds_list, deque):
                for remind in reminds_list:
                    if isinstance(remind, Remind):
                        self.reminds_list.append(remind)

        self.deadline = None
        if deadline is not None:
            self.deadline = deadline

        self.id = sha1(("Card: " + " " +
                        self.task.title + " " +
                        self.task.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        users_id = [user_id.hexdigest() for user_id in self.users_login]
        reminds_list = [remind for remind in self.reminds_list]

        if self.deadline is None:
            output = Colors.card_yellow + """
--- Card ---
ID: {}
Users ID: {}

Task:
{}

Reminds:
{}

---End Card--
""".format(self.id.hexdigest(),
           users_id,
           self.task,
           reminds_list) + Colors.end_color

        else:
            output = Colors.card_yellow + """
--- Card ---
ID: {}
Users ID: {}

Deadline:
{}

Is Repeatable: {}

Task:
{}

Reminds:
{}

---End Card--
""".format(self.id.hexdigest(),
           users_id,
           self.deadline.when_remind,
           self.deadline.is_repeatable,
           self.task,
           reminds_list) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id.hexdigest() for user_id in self.users_login]
        reminds_list = [remind for remind in self.reminds_list]

        if self.deadline is None:
            output = Colors.card_yellow + """
--- Card ---
ID: {}
Users ID: {}

Task:
{}

Reminds:
{}

---End Card--
""".format(self.id.hexdigest(),
           users_id,
           self.task,
           reminds_list) + Colors.end_color

        else:
            output = Colors.card_yellow + """
--- Card ---
ID: {}
Users ID: {}

Deadline:
{}

Is Repeatable: {}

Task:
{}

Reminds:
{}

---End Card--
""".format(self.id.hexdigest(),
           users_id,
           self.deadline.when_remind,
           self.deadline.is_repeatable,
           self.task,
           reminds_list) + Colors.end_color

        return output

    def update_card(self, task=None,
                    users: deque = None,
                    reminds_list: deque = None,
                    deadline: Remind = None):

        if task is not None:
            if isinstance(task, Task):
                self.task = task
            elif isinstance(task, str):
                self.task.title = task

        if users is not None:
            self.users_login.clear()
            self.users_login.append(users)

        if reminds_list is not None:
            self.reminds_list.clear()

            if isinstance(reminds_list, Remind):
                self.reminds_list.append(reminds_list)

            elif isinstance(reminds_list, deque):
                for remind in reminds_list:
                    if isinstance(remind, Remind):
                        self.reminds_list.append(remind)

        if deadline is not None:
            self.deadline = deadline

    def find_user_on_card(self, user_id: str = None,
                          user_name_surname: str = None,
                          user_nickname: str = None):

        if user_id is not None:
            try:
                return next(user for user in self.users_login if user.id == user_id)
            except StopIteration:
                return None

        elif user_name_surname is not None:
            try:
                return next(user for user in self.users_login if (user.name + " " + user.surname) == user_name_surname)
            except StopIteration:
                return None

        elif user_nickname is not None:
            try:
                return next(user for user in self.users_login if user.nickname == user_nickname)
            except StopIteration:
                return None

        else:
            return None

    def add_user_to_card(self, user_id: str):
        duplicate_user = self.find_user_on_card(user_nickname=user_id)

        if duplicate_user is None:
            self.users_login.append(user_id)

    def remove_user_from_card(self, user_id: str):
        duplicate_user = self.find_user_on_card(user_nickname=user_id)

        if duplicate_user is not None:
            self.users_login.remove(duplicate_user)

    def find_remind(self, title: str = None, remind_id: str = None):
        if title is not None:
            try:
                return next(remind for remind in self.reminds_list if remind.title == title)
            except StopIteration:
                return None

        elif remind_id is not None:
            try:
                return next(remind for remind in self.reminds_list if remind.id == remind_id)
            except StopIteration:
                return None

        else:
            return None

    def add_remind(self, remind: Remind):
        duplicate_remind = self.find_remind(remind_id=remind.id)

        if duplicate_remind is None:
            self.reminds_list.append(remind)

    def remove_remind(self, remind: Remind):
        duplicate_remind = self.find_remind(remind_id=remind.id)

        if duplicate_remind is not None:
            self.reminds_list.remove(duplicate_remind)

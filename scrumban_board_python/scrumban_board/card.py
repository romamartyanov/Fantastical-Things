from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.task import Task
from scrumban_board_python.scrumban_board.remind import Remind
from scrumban_board_python.scrumban_board.user import User


class Card:
    def __init__(self, task,
                 users: deque,
                 reminds_list: deque = None,
                 deadline: datetime.datetime = None,
                 repeatable_remind: datetime.timedelta = None):

        self.task = None
        if task is not None:
            if isinstance(task, Task):
                self.task = task
            elif isinstance(task, str):
                self.task = Task(title=task)

        self.users = deque()
        if users is not None:
            if isinstance(users, User):
                self.users.append(users)

            elif isinstance(users, deque):
                for user in users:
                    if isinstance(user, User):
                        self.users.append(users)

        self.reminds_list = deque()
        if reminds_list is not None:
            for remind in reminds_list:
                if isinstance(remind, Remind):
                    self.reminds_list.append(remind)

        self.deadline = None
        if deadline is not None:
            self.deadline = deadline

        self.repeatable_remind = None
        if repeatable_remind is not None:
            self.repeatable_remind = repeatable_remind

        self.id = sha1(("Card: " + " " +
                        self.task.title + " " +
                        self.task.description + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def update_card(self, task=None,
                    users: deque = None,
                    reminds_list: deque = None,
                    deadline: datetime.datetime = None,
                    repeatable_remind: datetime.timedelta = None):

        if task is not None:
            if isinstance(task, Task):
                self.task = task
            elif isinstance(task, str):
                self.task.title = task

        if users is not None:
            if isinstance(users, User):
                self.users.clear()
                self.users.append(users)

            elif isinstance(users, deque):
                self.users.clear()

                for user in users:
                    if isinstance(user, User):
                        self.users.append(users)

        if reminds_list is not None:
            self.reminds_list.clear()

            for remind in reminds_list:
                if isinstance(remind, Remind):
                    self.reminds_list.append(remind)

        if deadline is not None:
            self.deadline = deadline

        if repeatable_remind is not None:
            self.repeatable_remind = repeatable_remind

    def find_user_on_card(self, user_id: str = None,
                          user_name_surname: str = None,
                          user_nickname: str = None):

        if user_id is not None:
            return next(user for user in self.users if user.id == user_id)

        elif user_name_surname is not None:
            return next(user for user in self.users if (user.name + " " + user.surname) == user_name_surname)

        elif user_nickname is not None:
            return next(user for user in self.users if user.nickname == user_nickname)

        else:
            return None

    def add_user_to_card(self, user: User):
        duplicate_user = self.find_user_on_card(user_nickname=user.id)

        if duplicate_user is None:
            self.users.append(user)

    def remove_user_from_card(self, user: User):
        duplicate_user = self.find_user_on_card(user_nickname=user.id)

        if duplicate_user is not None:
            self.users.remove(duplicate_user)

    def find_remind(self, title: str = None, remind_id: str = None):
        if title is not None:
            return next(remind for remind in self.reminds_list if remind.title == title)

        elif remind_id is not None:
            return next(remind for remind in self.reminds_list if remind.id == remind_id)

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

import os
import logging.config
import string
import random

from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.task import Task
from scrumban_board_python.scrumban_board.remind import Remind
from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Card:
    """
    Card contains one Task and Reminds

    Example:
    card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind, reminds_list=remind)

    remind_list = deque()
    remind_list.append(remind)

    card.update_card(reminds_list=remind_list)
    """

    @staticmethod
    def get_task(task):
        if isinstance(task, Task):
            return task

        elif isinstance(task, str):
            task = Task(title=task)
            return task

    @staticmethod
    def get_users_login(users_login):
        if isinstance(users_login, deque):
            return users_login

        elif isinstance(users_login, str):
            users_login = deque()
            users_login.append(users_login)

            return users_login

    @staticmethod
    def get_remind_list(reminds_list):
        new_reminds_list = deque()

        if reminds_list is not None:
            if isinstance(reminds_list, Remind):
                new_reminds_list.append(reminds_list)

            elif isinstance(reminds_list, deque):
                for remind in reminds_list:
                    if isinstance(remind, Remind):
                        new_reminds_list.append(remind)

        return new_reminds_list

    @staticmethod
    def get_deadline(deadline):
        if deadline is not None:
            return deadline
        else:
            return None

    def __init__(self, task, users_login,
                 reminds_list=None, deadline: Remind = None):
        """
        Initialising of Card

        :param task: card task
        :param users_login: card users
        :param reminds_list: card reminds
        :param deadline: card deadline
        """

        self.task = Card.get_task(task)

        self.users_login = Card.get_users_login(users_login)
        self.reminds_list = Card.get_remind_list(reminds_list)

        self.deadline = Card.get_deadline(deadline)

        self.id = self._get_id()

        logger.info("Card ({}) was created".format(self.id))

    def _get_id(self):
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.task.title)))

        return sha1(("Card: " +
                     key + " " +
                     self.task.title + " " +
                     str(datetime.datetime.now())).encode('utf-8')).hexdigest()

    def __str__(self):
        users_id = [user_login for user_login in self.users_login]
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
        """.format(self.id,
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
        """.format(self.id,
                   users_id,
                   self.deadline.when_remind,
                   self.deadline.is_repeatable,
                   self.task,
                   reminds_list) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id for user_id in self.users_login]
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
            """.format(self.id,
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
            """.format(self.id,
                       users_id,
                       self.deadline.when_remind,
                       self.deadline.is_repeatable,
                       self.task,
                       reminds_list) + Colors.end_color

        return output

    def update_card(self, task=None,
                    users_login: deque = None,
                    reminds_list: deque = None,
                    deadline: Remind = None):
        """
        Updating card

        :param task: card task
        :param users_login: card users
        :param reminds_list: card reminds
        :param deadline: card deadline
        :return:
        """

        if task is not None:
            self.task = Card.get_task(task)

        if users_login is not None:
            self.users_login = Card.get_users_login(users_login)

        if reminds_list is not None:
            self.reminds_list = Card.get_remind_list(reminds_list)

        if deadline is not None:
            self.deadline = Card.get_deadline(deadline)

        logger.info("Card ({}) was updated".format(self.id))

    def find_user_on_card(self, user_login: str = None):
        """
        Searching user in the card

        :param user_login: searching user id
        :return:
        """

        if user_login is not None:
            try:
                user_login = next(user_login for user_login in self.users_login if user_login == user_login)
                logger.info("Users ({}) was found in the card ({})".format(user_login,
                                                                           self.id))
                return user_login

            except StopIteration:
                logger.info("Users ({}) wasn't found in the card ({})".format(user_login,
                                                                              self.id))

        else:
            return None

    def add_user_to_card(self, user_login: str):
        """
        Adding new user to the card

        :param user_login: user login
        :return:
        """
        duplicate_user = self.find_user_on_card(user_login=user_login)

        if duplicate_user is None:
            self.users_login.append(user_login)

            logger.info("Users ({}) was added to the card ({})".format(user_login,
                                                                       self.id))

    def remove_user_from_card(self, user_login: str):
        """
        Removing user from card

        :param user_login: user login
        :return:
        """
        duplicate_user = self.find_user_on_card(user_login=user_login)

        if duplicate_user is not None:
            self.users_login.remove(duplicate_user)

            logger.info("Users ({}) was removed from the card ({})".format(user_login,
                                                                           self.id))

    def find_remind(self, title: str = None, remind_id: str = None):
        """
        Searching remind in the card

        :param title:
        :param remind_id:
        :return:
        """
        if title is not None:
            try:
                remind = next(remind for remind in self.reminds_list if remind.title == title)
                logger.info("Remind ({}) was found by title in the card ({})".format(remind.title,
                                                                                     self.id))
                return remind

            except StopIteration:
                logger.info("Users ({}) wasn't found in the card ({})".format(title,
                                                                              self.id))

        elif remind_id is not None:
            try:
                remind = next(remind for remind in self.reminds_list if remind.id == remind_id)
                logger.info("Remind ({}) was found by remind_id in the card ({})".format(remind.id,
                                                                                         self.id))
                return remind

            except StopIteration:
                logger.info("Remind ({}) wasn't found by remind_id in the card ({})".format(remind_id,
                                                                                            self.id))
        return None

    def add_remind(self, remind: Remind):
        """
        Adding new remind to the card

        :param remind:
        :return:
        """
        duplicate_remind = self.find_remind(remind_id=remind.id)

        if duplicate_remind is None:
            self.reminds_list.append(remind)

            logger.info("Remind ({}) was added to the card ({})".format(remind.id,
                                                                        self.id))

    def remove_remind(self, remind: Remind):
        """
        Removing remind from the card

        :param remind:
        :return:
        """
        duplicate_remind = self.find_remind(remind_id=remind.id)

        if duplicate_remind is not None:
            self.reminds_list.remove(duplicate_remind)

            logger.info("Remind ({}) was removed from the card ({})".format(duplicate_remind.id,
                                                                            self.id))

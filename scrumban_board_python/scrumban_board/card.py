from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.task import Task
from scrumban_board_python.scrumban_board.remind import Remind
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Card:
    """
    Card contains one Task and Reminds

    Example:
    card = scrumban_board.Card(client.logger, task=task, users_login=user.login, deadline=remind, reminds_list=remind)

    remind_list = deque()
    remind_list.append(remind)

    card.update_card(reminds_list=remind_list)
    """

    def __init__(self, logger, task, users_login,
                 reminds_list=None, deadline: Remind = None):
        """
        Initialising of Card

        :param logger: client logger
        :param task: card task
        :param users_login: card users
        :param reminds_list: card reminds
        :param deadline: card deadline
        """

        self.logger = logger

        if isinstance(task, Task):
            self.task = task

        elif isinstance(task, str):
            task = Task(self.logger, title=task)
            self.task = task

        self.users_login = deque()
        if isinstance(users_login, deque):
            self.users_login = users_login
        elif isinstance(users_login, str):
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
                        str(datetime.datetime.now())).encode('utf-8')).hexdigest()

        self.logger.info("Card ({}) was created".format(self.id))

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
            if isinstance(task, Task):
                self.task = task
            elif isinstance(task, str):
                self.task.title = task

        if users_login is not None:
            self.users_login.clear()
            self.users_login.append(users_login)

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

        self.logger.info("Card ({}) was updated".format(self.id))

    def find_user_on_card(self, user_login: str = None):
        """
        Searching user in the card

        :param user_login: searching user id
        :return:
        """

        if user_login is not None:
            try:
                user_login = next(user_login for user_login in self.users_login if user_login == user_login)
                self.logger.info("Users ({}) was found in the card ({})".format(user_login,
                                                                                self.id))
                return user_login

            except StopIteration:
                self.logger.info("Users ({}) wasn't found in the card ({})".format(user_login,
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

            self.logger.info("Users ({}) was added to the card ({})".format(user_login,
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

            self.logger.info("Users ({}) was removed from the card ({})".format(user_login,
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
                self.logger.info("Remind ({}) was found by title in the card ({})".format(remind.title,
                                                                                          self.id))
                return remind

            except StopIteration:
                self.logger.info("Users ({}) wasn't found in the card ({})".format(title,
                                                                                   self.id))

        elif remind_id is not None:
            try:
                remind = next(remind for remind in self.reminds_list if remind.id == remind_id)
                self.logger.info("Remind ({}) was found by remind_id in the card ({})".format(remind.id,
                                                                                              self.id))
                return remind

            except StopIteration:
                self.logger.info("Remind ({}) wasn't found by remind_id in the card ({})".format(remind_id,
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

            self.logger.info("Remind ({}) was added to the card ({})".format(remind.id,
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

            self.logger.info("Remind ({}) was removed from the card ({})".format(duplicate_remind.id,
                                                                                 self.id))

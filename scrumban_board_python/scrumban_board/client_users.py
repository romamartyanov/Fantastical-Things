import os
import logging.config

from collections import deque

from scrumban_board_python.scrumban_board.user import User

logging.config.fileConfig(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logging.cfg'))
logger = logging.getLogger("ScrumbanBoard")


class ClientUsers:
    """
    ClientUsers in the class responsible for storing all the Users of the Client

    Example:

    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)
    """

    @staticmethod
    def _get_users(users):
        new_users = deque()

        if users is not None:
            for user in users:
                if isinstance(user, User):
                    new_users.append(user)

                elif isinstance(user, str):
                    temp_user = User(user, user, user, "@")
                    new_users.append(temp_user)

        return new_users

    def __init__(self, users: deque = None):
        """
        Initialising of ClientUsers

        :param users: Users for the storage
        """
        self.users = ClientUsers._get_users(users)

        logger.info("ClientUsers was created")

    def update_client_users(self, users: deque):
        """
        Updating object fields with new data

        :param users: new Users for the storage
        :return:
        """

        self.users = ClientUsers._get_users(users)

        logger.info("ClientUsers was updated")

    def find_user(self, user_id: str = None, user_login: str = None):
        """
        Searching User

        :param user_id: user_id for searching
        :param user_login: user_login for searching
        :return: User - if was found; None - if wasn't found
        """
        if user_id is not None:
            try:
                user = next(user for user in self.users if user.id == user_id)
                logger.info("User was found by user_id ({})".format(user_id))

                return user

            except StopIteration:
                logger.info("User wasn't found by user_id ({})".format(user_id))

        elif user_login is not None:
            try:
                user = next(user for user in self.users if user.login == user_login)
                logger.info("User was found by user_login ({})".format(user_login))

                return user

            except StopIteration:
                logger.info("User wasn't found by user_login ({})".format(user_login))

        return None

    def add_new_user(self, user):
        """
        Adding new User to self.users

        :param user: new User
        :return:
        """
        if isinstance(user, User):
            duplicate_user = self.find_user(user_id=user.id)

            if duplicate_user is None:
                self.users.append(user)
                logger.info("new User ({}) was added".format(user.id))

        elif isinstance(user, str):
            duplicate_user = self.find_user(user_login=user)

            if duplicate_user is None:
                temp_user = User(user, user, user, "none@none.none")

                self.users.append(temp_user)
                logger.info("new User ({}) was added".format(temp_user.id))

    def remove_user(self, user):
        """
        Removing User from self.users

        :param user: User or user.id or user.login
        :return:
        """
        if isinstance(user, User):
            duplicate_user = self.find_user(user_id=user.id)

            if duplicate_user is not None:
                self.users.remove(user)

                logger.info("User ({}) was removed".format(user.id))

        elif isinstance(user, str):
            duplicate_user_id = self.find_user(user_id=user)
            duplicate_user_login = self.find_user(user_login=user)

            if duplicate_user_id is not None:
                self.users.remove(duplicate_user_id)
                logger.info("User ({}) was removed".format(duplicate_user_id.id))

            elif duplicate_user_login is not None:
                self.users.remove(duplicate_user_login)
                logger.info("User ({}) was removed".format(duplicate_user_login.id))

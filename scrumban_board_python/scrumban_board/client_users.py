from collections import deque

from scrumban_board_python.scrumban_board.user import User


class ClientUsers:
    """
    ClientUsers in the class responsible for storing all the Users of the Client

    Example:

    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)
    """

    def __init__(self, logger, users: deque = None, ):
        """
        Initialising of ClientUsers

        :param logger: class logger
        :param users: Users for the storage
        """
        self.users = deque()
        self.logger = logger

        if users is not None:
            for user in users:
                if isinstance(user, User):
                    self.users.append(user)

                elif isinstance(user, str):
                    temp_user = User(self.logger, "", "", user, "")
                    self.users.append(temp_user)

        self.logger.info("ClientUsers was created")

    def update_client_users(self, users: deque):
        """
        Updating object fields with new data

        :param users: new Users for the storage
        :return:
        """

        self.users.clear()

        for user in users:
            if isinstance(user, User):
                self.users.append(user)

            elif isinstance(user, str):
                temp_user = User(self.logger, user, user, user, "@")
                self.users.append(temp_user)

        self.logger.info("ClientUsers was updated")

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
                self.logger.info("User was found by user_id ({})".format(user_id))

                return user

            except StopIteration:
                self.logger.info("User wasn't found by user_id ({})".format(user_id))

        elif user_login is not None:
            try:
                user = next(user for user in self.users if user.login == user_login)
                self.logger.info("User was found by user_login ({})".format(user_login))

                return user

            except StopIteration:
                self.logger.info("User wasn't found by user_login ({})".format(user_login))

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
                self.logger.info("new User ({}) was added".format(user.id))

        elif isinstance(user, str):
            duplicate_user = self.find_user(user_login=user)

            if duplicate_user is None:
                temp_user = User(self.logger, user, user, user, "none@none.none")

                self.users.append(temp_user)
                self.logger.info("new User ({}) was added".format(temp_user.id))

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

                self.logger.info("User ({}) was removed".format(user.id))

        elif isinstance(user, str):
            duplicate_user_id = self.find_user(user_id=user)
            duplicate_user_login = self.find_user(user_login=user)

            if duplicate_user_id is not None:
                self.users.remove(duplicate_user_id)
                self.logger.info("User ({}) was removed".format(duplicate_user_id.id))

            elif duplicate_user_login is not None:
                self.users.remove(duplicate_user_login)
                self.logger.info("User ({}) was removed".format(duplicate_user_login.id))

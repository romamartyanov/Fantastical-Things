from collections import deque

from scrumban_board_python.scrumban_board.user import User


class ClientUsers:
    def __init__(self, users: deque = None):
        self.users = deque()

        if users is not None:
            for user in users:
                if isinstance(user, User):
                    self.users.append(user)

                elif isinstance(user, str):
                    temp_user = User("", "", user, "")
                    self.users.append(temp_user)

    def update_client_users(self, users: deque):
        self.users.clear()

        for user in users:
            if isinstance(user, User):
                self.users.append(user)

            elif isinstance(user, str):
                temp_user = User(user, user, user, "@")
                self.users.append(temp_user)

    def find_user(self, user_id: str = None, user_login: str = None):
        if user_id is not None:
            try:
                return next(user for user in self.users if user.id == user_id)

            except StopIteration:
                return None

        elif user_login is not None:
            try:
                return next(user for user in self.users if user.login == user_login)

            except StopIteration:
                return None

    def add_new_user(self, user):
        if isinstance(user, User):
            duplicate_user = self.find_user(user_id=user.id)

            if duplicate_user is None:
                self.users.append(user)

        elif isinstance(user, str):
            duplicate_user = self.find_user(user_login=user)

            if duplicate_user is None:
                temp_user = User(user, user, user, "none@none.none")
                self.users.append(temp_user)

    def remove_user(self, user):
        if isinstance(user, User):
            duplicate_user = self.find_user(user_id=user.id)

            if duplicate_user is not None:
                self.users.remove(user)

        elif isinstance(user, str):
            duplicate_user_id = self.find_user(user_id=user)
            duplicate_user_login = self.find_user(user_login=user)

            if duplicate_user_id is not None:
                self.users.remove(duplicate_user_id)

            elif duplicate_user_login is not None:
                self.users.remove(duplicate_user_login)

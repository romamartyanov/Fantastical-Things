

class User:
    def __init__(self, name=None, surname=None, nickname=None, email=None):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.email = email

        self.calendar = None
        self.tasks = None
        self.teams_list = None

from hashlib import sha1
from collections import deque


class Team:
    def __init__(self, title: str, users: deque):
        self.users = []
        self.boards = []


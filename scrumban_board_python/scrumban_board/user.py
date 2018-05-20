from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.calendar import Calendar
from scrumban_board_python.scrumban_board.cardlist import CardList


class User:
    def __init__(self, name: str, surname: str, nickname: str, email: str,
                 boards: deque = None):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.email = email

        self.id = sha1(("User: " + " " +
                        self.nickname))

        u = deque()
        u.append(self)

        self.boards = deque()
        if boards is not None:
            for board in boards:
                if isinstance(board, Board):
                    self.boards.append(board)

        else:
            to_do = CardList("To-Do")
            doing = CardList("Doing")
            done = CardList("Done")

            l = deque()
            l.append(to_do)
            l.append(doing)
            l.append(done)

            board = Board("User Board", u, "default agile board", l)
            self.boards.append(board)

        self.calendar = Calendar(users=u)
        # self.teams_list = None

    def __str__(self):
        boards_id = [board_id.id for board_id in self.boards]

        output = """
Name: {}
Surname: {}
Nickname: {}
ID: {}
Email: {}

Boards ID: {}
""".format(self.name,
           self.surname,
           self.nickname,
           self.id,
           self.email,
           boards_id)

        return output

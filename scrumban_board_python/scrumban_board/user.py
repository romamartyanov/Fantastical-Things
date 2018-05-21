from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.user_calendar import Calendar
from scrumban_board_python.scrumban_board.cardlist import CardList
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class User:
    def __init__(self, name: str, surname: str, nickname: str, email: str,
                 boards: deque = None):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.email = email

        self.id = sha1(("User: " + " " +
                        self.nickname).encode('utf-8'))

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
            overdue = CardList("Overdue")

            l = deque()
            l.append(to_do)
            l.append(doing)
            l.append(done)
            l.append(overdue)

            board = Board("User Board", u, "default agile board", l)
            self.boards.append(board)

        self.calendar = Calendar(users=u)
        # self.teams_list = None

    def __str__(self):
        boards_id = [board_id.id.hexdigest() for board_id in self.boards]

        output = Colors.user_magenta + """
--- User ---
Name: {}
Surname: {}
Nickname: {}
ID: {}
Email: {}

Boards ID: {}
--End User--
""".format(self.name,
           self.surname,
           self.nickname,
           self.id.hexdigest(),
           self.email,
           boards_id) + Colors.ENDC

        return output

    def __repr__(self):
        boards_id = [board_id.id.hexdigest() for board_id in self.boards]

        output = Colors.user_magenta + """
--- User ---
Name: {}
Surname: {}
Nickname: {}
ID: {}
Email: {}

Boards ID: {}
--End User--
""".format(self.name,
           self.surname,
           self.nickname,
           self.id.hexdigest(),
           self.email,
           boards_id) + BColors.ENDC

        return output

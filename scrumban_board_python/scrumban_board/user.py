from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.calendar import Calendar
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class User:
    def __init__(self, name: str, surname: str, nickname: str, email: str,
                 user_boards=None, teams_id=None):

        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.email = email

        self.id = sha1(("User: " + " " +
                        self.nickname).encode('utf-8'))

        self.user_boards = deque()
        if user_boards is not None:
            if isinstance(user_boards, Board):
                self.user_boards.append(user_boards)

            elif isinstance(user_boards, deque):
                for board in user_boards:
                    if isinstance(board, Board):
                        self.user_boards.append(board)

        else:
            board = Board("{}'s Board".format(self.name), self.id, "default agile board")
            self.user_boards.append(board)

        self.user_calendar = Calendar(users_id=self.id)

        self.teams_list = deque()
        if teams_id is not None:
            for team_id in teams_id:
                if isinstance(team_id, str):
                    self.teams_list.append(team_id)

    def __str__(self):
        boards_id = [board_id.id.hexdigest() for board_id in self.user_boards]

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
           boards_id) + Colors.end_color

        return output

    def __repr__(self):
        boards_id = [board_id.id.hexdigest() for board_id in self.user_boards]

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
           boards_id) + Colors.end_color

        return output

    def update_user(self, name: str = None, surname: str = None, nickname: str = None, email: str = None,
                    user_boards=None, teams_id=None):

        if name is not None:
            self.name = name

        if surname is not None:
            self.surname = surname

        if nickname is not None:
            self.nickname = nickname

        if email is not None:
            self.email = email

        if user_boards is not None:
            self.user_boards.clear()

            if isinstance(user_boards, Board):
                self.user_boards.append(user_boards)

            elif isinstance(user_boards, deque):
                for board in user_boards:
                    if isinstance(board, Board):
                        self.user_boards.append(board)

        if teams_id is not None:
            self.teams_list.clear()

            for team_id in teams_id:
                if isinstance(team_id, str):
                    self.teams_list.append(team_id)

    def find_board(self, board_id: str = None, board_title: str = None):
        if board_id is not None:
            try:
                return next(board for board in self.user_boards if board.id == board_id)
            except StopIteration:
                return None

        elif board_title is not None:
            try:
                return next(board for board in self.user_boards if board.title == board_title)
            except StopIteration:
                return None

        else:
            return None

    def add_board(self, new_board: Board):
        duplicate_board = self.find_board(board_id=new_board.id)

        if duplicate_board is None:
            self.user_boards.append(new_board)

    def remove_board(self, board: Board = None, board_id: str = None):
        if board is not None:
            duplicate_board = self.find_board(board_id=board.id)

            if duplicate_board is not None:
                self.user_boards.remove(duplicate_board)

        elif board_id is not None:
            duplicate_board = self.find_board(board_id=board_id)

            if duplicate_board is not None:
                self.user_boards.remove(duplicate_board)

    def find_team_id(self, team_id: str):
        if team_id is not None:
            try:
                return next(team for team in self.teams_list if team == team_id)
            except StopIteration:
                return None

        else:
            return None

    def add_team_id(self, new_team_id: str):
        duplicate_team_id = self.find_team_id(team_id=new_team_id)

        if duplicate_team_id is None:
            self.teams_list.append(new_team_id)

    def remove_team_id(self, team_id: str):
        if team_id is not None:
            duplicate_team_id = self.find_team_id(team_id=team_id)

            if duplicate_team_id is not None:
                self.teams_list.remove(duplicate_team_id)

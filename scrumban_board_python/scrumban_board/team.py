from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Team:
    def __init__(self, title: str, nickname: str, users_id,
                 description: str = None, boards=None):

        self.title = title
        self.login = nickname

        if description is not None:
            self.description = description

        self.team_members_id = deque()
        if isinstance(users_id, str):
            self.team_members_id.append(users_id)

        elif isinstance(users_id, deque):
            for user_id in users_id:
                if isinstance(user_id, str):
                    self.team_members_id.append(user_id)

        self.team_boards = deque()
        if boards is not None:
            if isinstance(boards, Board):
                self.team_boards.append(boards)

            elif isinstance(boards, deque):
                for board in boards:
                    if isinstance(board, Board):
                        self.team_boards.append(board)

        else:
            board = Board("{}'s Board".format(self.title), self.id, "default agile board")
            self.team_boards.append(board)

        self.id = sha1(("Team: " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8'))

    def __str__(self):
        users_id = [user_id.hexdigest() for user_id in self.team_members_id]
        boards_id = [board.id.hexdigest() for board in self.team_boards]

        output = Colors.team_cyan + """
--- Team ---
Title: {}
Description: {}

Users ID:
{}

Boards ID:
{}

---End Team--
""".format(self.title,
           self.description,
           users_id,
           boards_id) + Colors.end_color

        return output

    def __repr__(self):
        users_id = [user_id.hexdigest() for user_id in self.team_members_id]
        boards_id = [board.id.hexdigest() for board in self.team_boards]

        output = Colors.team_cyan + """
--- Team ---
Title: {}
Description: {}

Users ID:
{}

Boards ID:
{}

---End Team--
""".format(self.title,
           self.description,
           users_id,
           boards_id) + Colors.end_color

        return output

    def update_team(self, title: str = None, users_id=None, description: str = None,
                    boards=None):

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if users_id is not None:
            self.team_members_id.clear()

            if isinstance(users_id, str):
                self.team_members_id.append(users_id)

            elif isinstance(users_id, deque):
                for user_id in users_id:
                    if isinstance(user_id, str):
                        self.team_members_id.append(user_id)

        if boards is not None:
            self.team_boards.clear()

            if isinstance(boards, Board):
                self.team_boards.append(boards)

            elif isinstance(boards, deque):
                for board in boards:
                    if isinstance(board, Board):
                        self.team_boards.append(board)

    def find_team_member(self, user_id: str):
        try:
            return next(team_user_id for team_user_id in self.team_members_id if team_user_id == user_id)

        except StopIteration:
            return None

    def add_team_member(self, user_id: str):
        duplicate_user = self.find_team_member(user_id)

        if duplicate_user is None:
            self.team_members_id.append(user_id)

    def remove_team_member(self, user_id: str):
        duplicate_user = self.find_team_member(user_id)

        if duplicate_user is not None:
            self.team_members_id.remove(duplicate_user)

    def find_team_board(self, board_id: str = None, board_title: str = None):
        if board_id is not None:
            try:
                return next(board for board in self.team_boards if board.id == board_id)

            except StopIteration:
                return None

        elif board_title is not None:
            try:
                return next(board for board in self.team_boards if board.id == board_title)

            except StopIteration:
                return None

    def add_team_board(self, board):
        if isinstance(board, str):
            duplicate_board = self.find_team_board(board)

            if duplicate_board is None:
                board = Board(title=board, users_id=self.team_members_id)
                self.team_boards.append(board)

        elif isinstance(board, Board):
            duplicate_board = self.find_team_board(board.id)

            if duplicate_board is None:
                self.team_boards.append(board)

    def remove_team_board(self, board):
        if isinstance(board, str):
            duplicate_board = self.find_team_board(board.id)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)

        elif isinstance(board, Board):
            duplicate_board = self.find_team_board(board.id)

            if duplicate_board is not None:
                self.team_boards.remove(board)

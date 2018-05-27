import os
import logging.config
import string
import random
import datetime

from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Team:
    """
    Description of the essence of the Team and his ability to interact with other classes

    Example:
    team = scrumban_board.Team("200 OK", "200_OK", "romamartyanov")

    client.client_teams.add_new_team(team)
    """

    @staticmethod
    def _get_team_boards(login, boards=None):
        new_team_boards = deque()

        if boards is not None:
            if isinstance(boards, Board):
                new_team_boards.append(boards)

            elif isinstance(boards, deque):
                for board in boards:
                    if isinstance(board, Board):
                        new_team_boards.append(board)
        else:
            board = Board("Agile Board", login, "default agile board")
            new_team_boards.append(board)

        return new_team_boards

    @staticmethod
    def _get_team_members_login(users_login):
        if isinstance(users_login, deque):
            return users_login

        elif isinstance(users_login, str):
            users_login = deque()
            users_login.append(users_login)

            return users_login

    def __init__(self, title: str, login: str, users_login,
                 description: str = None, boards=None):
        """
        Initialising of Team

        :param title: team title
        :param login: team login
        :param users_login: team users (deque or str)
        :param description: team description
        :param boards: team boards (deque or Board)
        """

        self.title = title
        self.login = login

        if description is not None:
            self.description = description

        self.team_members_login = Team._get_team_members_login(users_login)
        self.team_boards = Team._get_team_boards(login, boards)

        self.id = self._get_id()

        logger.info("Team ({}) was created".format(self.id))

    def _get_id(self):
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.login)))

        return sha1(("Team: " +
                     key + " " +
                     self.login + " " +
                     str(datetime.datetime.now())).encode('utf-8')).hexdigest()

    def __str__(self):
        users_id = [user_id for user_id in self.team_members_login]
        boards_id = [board.id for board in self.team_boards]

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
        users_id = [user_id for user_id in self.team_members_login]
        boards_id = [board.id for board in self.team_boards]

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

    def update_team(self, title: str = None, users_login=None, description: str = None,
                    boards=None):

        """
        Updating Team params

        :param title: team title
        :param users_login: team users (deque or str)
        :param description: team description
        :param boards: team boards (deque or Board)
        :return:
        """

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if users_login is not None:
            self.team_members_login = Team._get_team_members_login(users_login)

        if boards is not None:
            self.team_boards = Team._get_team_boards(self.login, boards)

        logger.info("Team ({}) was updated".format(self.id))

    def find_team_member(self, users_login: str):
        """
        Searchinf team member

        :param users_login: team member id
        :return:
        """
        try:
            users_login = next(team_user_id for team_user_id in self.team_members_login if team_user_id == users_login)
            logger.info("User ({}) was found by user_id in the Team ({})".format(users_login,
                                                                                 self.id))

            return users_login

        except StopIteration:
            logger.info("User ({}) wasn't found by user_id on Team ({})".format(users_login,
                                                                                self.id))
        return None

    def add_team_member(self, users_login: str):
        """
        Adding new team member

        :param users_login: user id
        :return:
        """
        duplicate_user = self.find_team_member(users_login)

        if duplicate_user is None:
            self.team_members_login.append(users_login)
            logger.info("User ({}) was added in the Team ({})".format(users_login,
                                                                      self.id))

    def remove_team_member(self, users_login: str):
        """
        Removing team member

        :param users_login: user id
        :return:
        """
        duplicate_user = self.find_team_member(users_login)

        if duplicate_user is not None:
            self.team_members_login.remove(duplicate_user)
            logger.info("User ({}) was removed from the Team ({})".format(duplicate_user,
                                                                          self.id))

    def find_team_board(self, board_id: str = None, board_title: str = None):
        """
        Seaching team boards

        :param board_id: board id
        :param board_title: board title
        :return:
        """
        if board_id is not None:
            try:
                board = next(board for board in self.team_boards if board.id == board_id)
                return board

            except StopIteration:
                logger.info("Board ({}) wasn't found by board_id in User({})".format(board_id,
                                                                                     self.id))

        elif board_title is not None:
            try:
                board = next(board for board in self.team_boards if board.id == board_title)
                return board

            except StopIteration:
                logger.info("Board ({}) wasn't found by board_title in User({})".format(board_title,
                                                                                        self.id))

        return None

    def add_team_board(self, board):
        """
        Adding new team board

        :param board: new board (Board or board title as str)
        :return:
        """
        if isinstance(board, str):
            duplicate_board = self.find_team_board(board)

            if duplicate_board is None:
                board = Board(title=board, users_login=self.team_members_login)
                self.team_boards.append(board)

                logger.info("Board ({}) was added to the Team ({})".format(board.id,
                                                                           self.id))

        elif isinstance(board, Board):
            duplicate_board = self.find_team_board(board.id)

            if duplicate_board is None:
                self.team_boards.append(board)

                logger.info("Board ({}) was added to the Team ({})".format(board.id,
                                                                           self.id))

    def remove_team_board(self, board: Board = None, board_id: str = None, board_title: str = None):
        """
        Removing board from the team

        :param board: Board
        :param board_id: board id
        :param board_title: board title
        :return:
        """
        if isinstance(board, Board):
            duplicate_board = self.find_team_board(board_id=board.id)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)

                logger.info("Board ({}) was removed to the Team ({})".format(duplicate_board.id,
                                                                             self.id))

        elif isinstance(board_id, str):
            duplicate_board = self.find_team_board(board_id=board_id)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)
                logger.info("Board ({}) was removed by board_id to the Team ({})".format(duplicate_board.id,
                                                                                         self.id))

        elif isinstance(board_title, str):
            duplicate_board = self.find_team_board(board_title=board_title)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)
                logger.info("Board ({}) was removed by board_title to the Team ({})".format(duplicate_board.id,
                                                                                            self.id))

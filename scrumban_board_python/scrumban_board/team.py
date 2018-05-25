from hashlib import sha1
from collections import deque
import datetime

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class Team:
    """
    Description of the essence of the Team and his ability to interact with other classes

    Example:
    team = scrumban_board.Team(client.logger, "200 OK", "200_OK", "romamartyanov")

    client.client_teams.add_new_team(team)
    """

    def __init__(self, logger, title: str, login: str, users_id,
                 description: str = None, boards=None):
        """
        Initialising of Team


        :param logger: client logger
        :param title: team title
        :param login: team login
        :param users_id: team users (deque or str)
        :param description: team description
        :param boards: team boards (deque or Board)
        """

        self.title = title
        self.login = login

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
            board = Board(self.logger, "{}'s Board".format(self.title), self.id, "default agile board")
            self.team_boards.append(board)

        self.id = sha1(("Team: " +
                        self.title + " " +
                        str(datetime.datetime.now())).encode('utf-8')).hexdigest()

        self.logger = logger
        self.logger.info("Team ({}) was created".format(self.id))

    def __str__(self):
        users_id = [user_id for user_id in self.team_members_id]
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
        users_id = [user_id for user_id in self.team_members_id]
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

    def update_team(self, title: str = None, users_id=None, description: str = None,
                    boards=None):

        """
        Updating Team params

        :param title: team title
        :param users_id: team users (deque or str)
        :param description: team description
        :param boards: team boards (deque or Board)
        :return:
        """

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

        self.logger.info("Team ({}) was updated".format(self.id))

    def find_team_member(self, user_id: str):
        """
        Searchinf team member

        :param user_id: team member id
        :return:
        """
        try:
            user_id = next(team_user_id for team_user_id in self.team_members_id if team_user_id == user_id)
            self.logger.info("User ({}) was found by user_id in the Team ({})".format(user_id,
                                                                                      self.id))

            return user_id

        except StopIteration:
            self.logger.info("User ({}) wasn't found by user_id on Team ({})".format(user_id,
                                                                                     self.id))
        return None

    def add_team_member(self, user_id: str):
        """
        Adding new team member

        :param user_id: user id
        :return:
        """
        duplicate_user = self.find_team_member(user_id)

        if duplicate_user is None:
            self.team_members_id.append(user_id)
            self.logger.info("User ({}) was added in the Team ({})".format(user_id,
                                                                           self.id))

    def remove_team_member(self, user_id: str):
        """
        Removing team member

        :param user_id: user id
        :return:
        """
        duplicate_user = self.find_team_member(user_id)

        if duplicate_user is not None:
            self.team_members_id.remove(duplicate_user)
            self.logger.info("User ({}) was removed from the Team ({})".format(duplicate_user,
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
                self.logger.info("Board ({}) wasn't found by board_id in User({})".format(board_id,
                                                                                          self.id))

        elif board_title is not None:
            try:
                board = next(board for board in self.team_boards if board.id == board_title)
                return board

            except StopIteration:
                self.logger.info("Board ({}) wasn't found by board_title in User({})".format(board_title,
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
                board = Board(logger=self.logger, title=board, users_login=self.team_members_id)
                self.team_boards.append(board)

                self.logger.info("Board ({}) was added to the Team ({})".format(board.id,
                                                                                self.id))

        elif isinstance(board, Board):
            duplicate_board = self.find_team_board(board.id)

            if duplicate_board is None:
                self.team_boards.append(board)

                self.logger.info("Board ({}) was added to the Team ({})".format(board.id,
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

                self.logger.info("Board ({}) was removed to the Team ({})".format(duplicate_board.id,
                                                                                  self.id))

        elif isinstance(board_id, str):
            duplicate_board = self.find_team_board(board_id=board_id)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)
                self.logger.info("Board ({}) was removed by board_id to the Team ({})".format(duplicate_board.id,
                                                                                              self.id))

        elif isinstance(board_title, str):
            duplicate_board = self.find_team_board(board_title=board_title)
            if duplicate_board is not None:
                self.team_boards.remove(duplicate_board)
                self.logger.info("Board ({}) was removed by board_title to the Team ({})".format(duplicate_board.id,
                                                                                                 self.id))

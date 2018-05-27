import os
import logging.config
import string
import random

from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.terminal_colors import Colors

logging.config.fileConfig(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logging.cfg'))
logger = logging.getLogger("ScrumbanBoard")


class User:
    """
    Description of the essence of the User and his ability to interact with other classes

    Example:
    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)

    task = scrumban_board.Task("title", "description")
    task.add_subtask(scrumban_board.Subtask("subtask1"))
    task.add_subtask(scrumban_board.Subtask("subtask2"))

    remind = scrumban_board.Remind("Remind", datetime.now(),
                                   repeating_remind_relativedelta=relativedelta(minutes=+2))

    card = scrumban_board.Card(task=task, users_login=user.login, deadline=remind, reminds_list=remind)

    remind_list = deque()
    remind_list.append(remind)

    card.update_card(reminds_list=remind_list)

    for board in user.user_boards:
        for cardlist in board.cardlists:
            cardlist.add_card(card)
            break
    """

    @staticmethod
    def _get_user_boards(login, boards=None):
        new_user_boards = deque()

        if boards is not None:
            if isinstance(boards, Board):
                new_user_boards.append(boards)

            elif isinstance(boards, deque):
                for board in boards:
                    if isinstance(board, Board):
                        new_user_boards.append(board)
        else:
            board = Board("Agile Board", login, "default agile board")
            new_user_boards.append(board)

        return new_user_boards

    @staticmethod
    def _get_teams_list(teams_id=None):
        teams_list = deque()

        if teams_id is not None:
            for team_id in teams_id:
                if isinstance(team_id, str):
                    teams_list.append(team_id)

        return teams_list

    def __init__(self, name: str, surname: str, nickname: str, email: str,
                 user_boards=None, teams_id=None):
        """
        Initialising of User

        :param name: User name
        :param surname: User surname
        :param nickname: User nickname
        :param email: User email
        :param user_boards: User boards (or one board, or no boards - default boards will be created)
        :param teams_id: User teams (or no teams)
        """

        self.name = name
        self.surname = surname
        self.login = nickname
        self.email = email

        self.user_boards = User._get_user_boards(self.login, user_boards)
        self.teams_id = User._get_teams_list(teams_id)

        self.id = self._get_id()

        logger.info("User ({}) was created".format(self.id))

    def _get_id(self):
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(self.login)))

        return sha1(("User: " +
                     key + " " +
                     self.login).encode('utf-8')).hexdigest()

    def __str__(self):
        boards_id = [board_id.id for board_id in self.user_boards]

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
           self.login,
           self.id,
           self.email,
           boards_id) + Colors.end_color

        return output

    def __repr__(self):
        boards_id = [board_id.id for board_id in self.user_boards]

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
           self.login,
           self.id,
           self.email,
           boards_id) + Colors.end_color

        return output

    def update_user(self, name: str = None, surname: str = None, email: str = None,
                    user_boards=None, teams_id=None):
        """

        Updating User params

        :param name: User name
        :param surname: User surname
        :param email: User email
        :param user_boards: User boards (or one board, or no boards - default boards will be created)
        :param teams_id: User teams (or no teams)
        :return:
        """

        if name is not None:
            self.name = name

        if surname is not None:
            self.surname = surname

        if email is not None:
            self.email = email

        if user_boards is not None:
            self.user_boards = User._get_user_boards(self.login, user_boards)

        if teams_id is not None:
            self.teams_id = User._get_teams_list(teams_id)

        logger.info("User ({}) was updated".format(self.id))

    def find_board(self, board_id: str = None, board_title: str = None):
        """
        Searching board in this user

        :param board_id: board id
        :param board_title: board title
        :return:
        """
        if board_id is not None:
            try:
                board = next(board for board in self.user_boards if board.id == board_id)
                logger.info("Border ({}) was found by board_id on User ({})".format(board_id,
                                                                                    self.id))

                return board
            except StopIteration:
                logger.info("Border ({}) wasn't found by board_id on User ({})".format(board_id,
                                                                                       self.id))

        elif board_title is not None:
            try:
                board = next(board for board in self.user_boards if board.title == board_title)
                logger.info("Border ({}) was found by board_title on User ({})".format(board_title,
                                                                                       self.id))

                return board

            except StopIteration:
                logger.info("Border ({}) wasn't found by board_title on User ({})".format(board_title,
                                                                                          self.id))

        return None

    def add_board(self, new_board):
        """
        Adding new board to the user

        :param new_board: new Board
        :return:
        """

        if isinstance(new_board, Board):
            duplicate_board = self.find_board(board_id=new_board.id)

            if duplicate_board is None:
                self.user_boards.append(new_board)

                logger.info("Border ({}) was added to User ({})".format(new_board.id,
                                                                        self.id))

        elif isinstance(new_board, str):
            duplicate_board = self.find_board(board_title=new_board)

            if duplicate_board is None:
                board = Board(title=new_board, users_login=self.id)
                self.user_boards.append(board)

                logger.info("Board ({}) was added to the Team ({})".format(board.id,
                                                                           self.id))

    def remove_board(self, board: Board = None, board_id: str = None):
        """
        Removing board in this user

        :param board: board
        :param board_id: board id
        :return:
        """
        if board is not None:
            duplicate_board = self.find_board(board_id=board.id)

            if duplicate_board is not None:
                self.user_boards.remove(duplicate_board)
                logger.info("Border ({}) was removed from User ({})".format(duplicate_board.id,
                                                                            self.id))

        elif board_id is not None:
            duplicate_board = self.find_board(board_id=board_id)

            if duplicate_board is not None:
                self.user_boards.remove(duplicate_board)
                logger.info("Border ({}) was removed from User ({})".format(duplicate_board.id,
                                                                            self.id))

    def find_team_id(self, team_id: str = None, team_login: str = None):
        """
        Searching teams id in this user

        :param team_id: team id
        :param team_login: team login
        :return:
        """
        if team_id is not None:
            try:
                team = next(team for team in self.teams_id if team.id == team_id)
                logger.info("Team ({}) was found by team_id in User({})".format(team_id,
                                                                                self.id))
                return team

            except StopIteration:
                logger.info("Team ({}) wasn't found by team_id in User({})".format(team_id,
                                                                                   self.id))

        elif team_login is not None:
            try:
                team = next(team for team in self.teams_id if team.login == team_login)
                logger.info("Team ({}) was found by team_login in User({})".format(team_login,
                                                                                   self.id))
                return team

            except StopIteration:
                logger.info("Team ({}) wasn't found by team_login in User({})".format(team_login,
                                                                                      self.id))
        return None

    def add_team_id(self, new_team_id: str):
        """
        Adding new team id to the user

        :param new_team_id: id of new team
        :return:
        """
        duplicate_team_id = self.find_team_id(team_id=new_team_id)

        if duplicate_team_id is None:
            self.teams_id.append(new_team_id)

            logger.info("Team ({}) was added by to User({})".format(new_team_id,
                                                                    self.id))

    def remove_team_id(self, team_id: str):
        """
        Removing team id in user

        :param team_id: team id
        :return:
        """
        if team_id is not None:
            duplicate_team_id = self.find_team_id(team_id=team_id)

            if duplicate_team_id is not None:
                self.teams_id.remove(duplicate_team_id)

                logger.info("Team ({}) was removed by in User({})".format(duplicate_team_id,
                                                                          self.id))

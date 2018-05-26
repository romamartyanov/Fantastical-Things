from hashlib import sha1
from collections import deque

from scrumban_board_python.scrumban_board.board import Board
from scrumban_board_python.scrumban_board.terminal_colors import Colors


class User:
    """
    Description of the essence of the User and his ability to interact with other classes

    Example:
    user = scrumban_board.User(client.logger, "Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
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

    def __init__(self, logger, name: str, surname: str, nickname: str, email: str,
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
        self.logger = logger

        self.id = sha1(("User: " + " " +
                        self.login).encode('utf-8')).hexdigest()

        self.user_boards = deque()
        if user_boards is not None:
            if isinstance(user_boards, Board):
                self.user_boards.append(user_boards)

            elif isinstance(user_boards, deque):
                for board in user_boards:
                    if isinstance(board, Board):
                        self.user_boards.append(board)

        else:
            board = Board(self.logger, "{}'s Board".format(self.name), self.login, "default agile board")
            self.user_boards.append(board)

        # self.user_calendar = Calendar(users_id=self.id)

        self.teams_list = deque()
        if teams_id is not None:
            for team_id in teams_id:
                if isinstance(team_id, str):
                    self.teams_list.append(team_id)

        self.logger.info("User ({}) was created".format(self.id))

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

        self.logger.info("User ({}) was updated".format(self.id))

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
                self.logger.info("Border ({}) was found by board_id on User ({})".format(board_id,
                                                                                         self.id))

                return board
            except StopIteration:
                self.logger.info("Border ({}) wasn't found by board_id on User ({})".format(board_id,
                                                                                            self.id))

        elif board_title is not None:
            try:
                board = next(board for board in self.user_boards if board.title == board_title)
                self.logger.info("Border ({}) was found by board_title on User ({})".format(board_title,
                                                                                            self.id))

                return board

            except StopIteration:
                self.logger.info("Border ({}) wasn't found by board_title on User ({})".format(board_title,
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

                self.logger.info("Border ({}) was added to User ({})".format(new_board.id,
                                                                             self.id))

        elif isinstance(new_board, str):
            duplicate_board = self.find_board(board_title=new_board)

            if duplicate_board is None:
                board = Board(logger=self.logger, title=new_board, users_login=self.id)
                self.user_boards.append(board)

                self.logger.info("Board ({}) was added to the Team ({})".format(board.id,
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
                self.logger.info("Border ({}) was removed from User ({})".format(duplicate_board.id,
                                                                                 self.id))

        elif board_id is not None:
            duplicate_board = self.find_board(board_id=board_id)

            if duplicate_board is not None:
                self.user_boards.remove(duplicate_board)
                self.logger.info("Border ({}) was removed from User ({})".format(duplicate_board.id,
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
                team = next(team for team in self.teams_list if team.id == team_id)
                self.logger.info("Team ({}) was found by team_id in User({})".format(team_id,
                                                                                     self.id))
                return team

            except StopIteration:
                self.logger.info("Team ({}) wasn't found by team_id in User({})".format(team_id,
                                                                                        self.id))

        elif team_login is not None:
            try:
                team = next(team for team in self.teams_list if team.login == team_login)
                self.logger.info("Team ({}) was found by team_login in User({})".format(team_login,
                                                                                        self.id))
                return team

            except StopIteration:
                self.logger.info("Team ({}) wasn't found by team_login in User({})".format(team_login,
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
            self.teams_list.append(new_team_id)

            self.logger.info("Team ({}) was added by to User({})".format(new_team_id,
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
                self.teams_list.remove(duplicate_team_id)

                self.logger.info("Team ({}) was removed by in User({})".format(duplicate_team_id,
                                                                               self.id))

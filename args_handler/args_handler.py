import argparse
import logging.config

import json
import jsonpickle

from scrumban_board_python import scrumban_board

logging.config.fileConfig('args_handler_logging.cfg')
logger = logging.getLogger("ArgsHandler")


class ArgsHandler:
    def __init__(self):
        with open('client.json', 'r') as infile:
            data = json.load(infile)

        self.client = jsonpickle.decode(data)

        while not self.client.update_all_reminds():
            continue

        self.current_user = self.client.client_users.find_user(user_login=self.client.current_user_login)

        self.current_user_teams = list()
        for team in self.client.client_teams.teams:
            for user_team_id in self.current_user.teams_id:
                if team.id == user_team_id:
                    self.current_user_teams.append(team)

    ###

        parser = argparse.ArgumentParser()

        parser.add_argument('--show_current_user', action='store_true',
                            help='Show Current user')

        parser.add_argument('--show_current_user_teams', action='store_true',
                            help='Show Teams of Current user')

        parser.add_argument('--show_board', action="store",
                            help='Show Board of current user: board id')

        parser.add_argument('--show_cardlist', action="store",
                            help='Show Cardlist of current user: cardlist id')

        parser.add_argument('--show_card', action="store",
                            help='Show Card of current user: card id')

        parser.add_argument('--show_task', action="store",
                            help='Show Task of current user: task id')

        parser.add_argument('--show_remind', action="store",
                            help='Show Remind of current user: remind id')

        parser.add_argument('--show_subtask', action="store",
                            help='Show Subask of current user: subtask id')

    ###

        parser.add_argument('--create_board_where', action="store",
                            help='Create Board: Team id')

        parser.add_argument('--create_board', action="store_true",
                            help='Creating to Current user')

        parser.add_argument('--board_title', action="store",
                            help='Board title: str')

    ###

        parser.add_argument('--create_cardlist_where', action="store",
                            help='Create Cardlist to Board: Board id')

        parser.add_argument('--cardlist_title', action="store",
                            help='Cardlist_title: str')

        parser.add_argument('--cardlist_description', action="store",
                            help='Cardlist description: str')

    ###

        parser.add_argument('--create_card_where', action="store",
                            help='Create Card to Cardlist: cardlist id')

        parser.add_argument('--card_deadline', action="store",
                            help='Card deadlile: format %Y/%m/%d-%H:%M or %Y/%m/%d')

        parser.add_argument('--card_repeatable_time', action="store",
                            help='Card Repeatable Time: format years=1 or months=2 or days=3 or hours=5 or minutes=6')

    ###

        parser.add_argument('--create_task_where', action="store",
                            help='Create Task to Card: card id')

        parser.add_argument('--task_title', action="store",
                            help='Task title: str')

        parser.add_argument('--task_description', action="store",
                            help='Task description: str')

        parser.add_argument('--task_completed', action="store",
                            help='Task completed: True or False')

    ###

        parser.add_argument('--create_subtask_where', action="store",
                            help='Create Subtask to Task: task id')

        parser.add_argument('--subtask_title', action="store",
                            help='Subtask title: str')

        parser.add_argument('--subtask_description', action="store",
                            help='Subtask description: str')

        parser.add_argument('--subtask_completed', action="store",
                            help='Subtask completed: True or False')

    ###

        args = parser.parse_args()

        if args.show_current_user:
            self.show_curren_user()

        if args.show_current_user_teams:
            self.show_current_user_teams()

        if args.show_board is not None:
            self.show_board(args.show_board)

        if args.show_cardlist is not None:
            self.show_cardlist(args.show_cardlist)

        if args.show_card is not None:
            self.show_card(args.show_card)

        if args.show_task is not None:
            self.show_task(args.show_task)

        if args.show_subtask is not None:
            self.show_subtask(args.show_subtask)

    ###

        if args.create_board:
            if args.board_title is not None:
                self.create_board(args.board_title)

                print(self.current_user)

        if args.create_board_where is not None:
            if args.board_title is not None:
                self.create_team_board(args.create_board_where, args.board_title)

        if args.create_cardlist_where is not None:
            if args.cardlist_title is not None:
                self.create_cardlist_where(cardlist_title=args.cardlist_title,
                                           board_id=args.create_cardlist_where,
                                           cardlist_description=args.cardlist_description)

        if args.create_card_where is not None:
            if args.task_title is not None:
                self.create_card_where(task_title=args.task_title,
                                       cardlist_id=args.create_cardlist_where,
                                       task_description=args.task_description,
                                       deadline=args.card_deadline,
                                       repeatable_time=args.card_repeatable_time)

        if args.create_subtask_where is not None:
            if args.subtask_title is not None:
                self.create_subtask_where(subtask_title=args.subtask_title,
                                          task_id=args.create_subtask_where,
                                          subtask_description=args.subtask_description)

###

    def _get_board(self, board_id):
        return self.current_user.find_board(board_id=board_id)

    def _get_cardlist(self, cardlist_id):
        for board in self.current_user.user_boards:
            return board.find_cardlist(cardlist_id=cardlist_id)

    def _ger_card(self, card_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                return cardlist.find_card(card_id=card_id)

    def _get_task(self, task_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                for card in cardlist.cards:
                    if card.task.id == task_id:
                        return card.task

    def _get_subtask(self, subtask_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                for card in cardlist.cards:
                    return card.task.find_subtask(subtask_id=subtask_id)

###

    def show_curren_user(self):
        print(self.current_user)

    def show_current_user_teams(self):
        for team in self.current_user_teams:
            print(team)

    def show_board(self, board_id):
        board = self._get_board(board_id)
        if board is not None:
            print(board)

    def show_cardlist(self, cardlist_id):
        cardlist = self._get_cardlist(cardlist_id)
        if cardlist is not None:
            print(cardlist)

    def show_card(self, card_id):
        card = self._ger_card(card_id)
        if card is not None:
            print(card)

    def show_task(self, task_id):
        task = self._get_task(task_id)
        if task is not None:
            print(task)

    def show_subtask(self, subtask_id):
        subtask = self._get_subtask(subtask_id)
        if subtask is not None:
            print(subtask)

###

    def create_board(self, board_title):
        self.current_user.add_board(board_title)

    def create_team_board(self, team_id, board_title):
        for team in self.current_user_teams:
            if team.id == team_id:
                team_members_login = [login for login in team.team_members_login]
                board = scrumban_board.Board(title=board_title, users_login=team_members_login)

                team.add_team_board(board)

    def create_cardlist_where(self, cardlist_title, board_id, cardlist_description=None):
        board = self._get_board(board_id=board_id)

        if board is not None:
            cardlist = scrumban_board.CardList(title=cardlist_title, description=cardlist_description)
            board.add_cardlist(cardlist)

    def create_card_where(self, task_title, cardlist_id, task_description=None, deadline=None,
                          repeatable_time=None):
        cardlist = self._get_cardlist(cardlist_id)

        if cardlist_id is not None:
            task = scrumban_board.Task(title=task_title, description=task_description)

            deadline = scrumban_board.Remind(title=task_title, when_remind=deadline,
                                             repeatable_time=repeatable_time)

            card = scrumban_board.Card(task=task, users_login=self.current_user.id, deadline=deadline)
            cardlist.add_card(card)

    def create_subtask_where(self, subtask_title, task_id, subtask_description=None):
        task = self._get_task(task_id)

        if task is not None:
            task.add_subtask(scrumban_board.Subtask(title=subtask_title, description=subtask_description))

###

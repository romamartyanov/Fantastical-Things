import argparse
import logging.config

import json
import jsonpickle

from scrumban_board_python import scrumban_board

logging.config.fileConfig('args_handler_logging.cfg')
logger = logging.getLogger("ArgsHandler")


class ArgsHandler:
    def __init__(self):
        try:

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

            #####################

            parser = argparse.ArgumentParser()
            subparsers = parser.add_subparsers(help='Subparsers')

            show_group = subparsers.add_parser('show')
            create_group = subparsers.add_parser('create')
            update_group = subparsers.add_parser('update')
            remove_group = subparsers.add_parser('remove')

            show_group.set_defaults(which='show')
            create_group.set_defaults(which='create')
            update_group.set_defaults(which='update')
            remove_group.set_defaults(which='remove')

            subparsers = show_group.add_subparsers()

            user_show = subparsers.add_parser('user')
            user_show.set_defaults(which='show_user')
            user_show.add_argument('current_user', action='store_true',
                                   help='Show Current user')

            user_teams_show = subparsers.add_parser('user_teams')
            user_teams_show.set_defaults(which='show_user_teams')
            user_teams_show.add_argument('current_user_teams', action='store_true',
                                         help='Show Teams of Current user')

            ###

            board_show = subparsers.add_parser('board')
            board_show.set_defaults(which='show_board')
            board_show.add_argument('board_id', action="store",
                                    help='Show Board of current user: board id')

            cardlist_show = subparsers.add_parser('cardlist')
            cardlist_show.set_defaults(which='show_cardlist')
            cardlist_show.add_argument('cardlist_id', action="store",
                                       help='Show Cardlist of current user: cardlist id')

            card_show = subparsers.add_parser('card')
            card_show.set_defaults(which='show_card')
            card_show.add_argument('card_id', action="store",
                                   help='Show Card of current user: card id')

            task_show = subparsers.add_parser('task')
            task_show.set_defaults(which='show_task')
            task_show.add_argument('task_id', action="store",
                                   help='Show Task of current user: task id')

            # remind_show = subparsers.add_parser('remind')
            # remind_show.set_defaults(which='show_remind')
            # remind_show.add_argument('remind_id', action="store",
            #                          help='Show Remind of current user: remind id')

            subtask_show = subparsers.add_parser('subtask')
            subtask_show.set_defaults(which='show_subtask')
            subtask_show.add_argument('subtask_id', action="store",
                                      help='Show Subask of current user: subtask id')

            #####################

            subparsers = create_group.add_subparsers()

            board_create = subparsers.add_parser('board')
            board_create.set_defaults(which='create_board')
            board_create.add_argument('--team_id', action='store',
                                      help='Team Id where to create board')

            board_create.add_argument('board_title', action='store',
                                      help='Board title')

            board_create.add_argument('--board_description', action='store',
                                      help='Board description')

            ###

            cardlist_create = subparsers.add_parser('cardlist')
            cardlist_create.set_defaults(which='create_cardlist')

            cardlist_create.add_argument('board_id', action='store',
                                         help='Board ID where to create cardlist')

            cardlist_create.add_argument('cardlist_title', action='store',
                                         help='Cardlist title')

            cardlist_create.add_argument('--cardlist_description', action='store',
                                         help='Cardlist description')

            ###

            card_create = subparsers.add_parser('card')
            card_create.set_defaults(which='create_card')

            card_create.add_argument('cardlist_id', action='store',
                                     help='Cardlist ID where to create card')

            card_create.add_argument('card_title', action='store',
                                     help='Card title')

            card_create.add_argument('--card_description', action='store',
                                     help='Card description')

            card_create.add_argument('--card_deadline', action="store",
                                     help='Card deadlile: format %%Y/%%m/%%d-%%H:%%M or %%Y/%%m/%%d')

            card_create.add_argument('--card_repeatable_time', action="store",
                                     help='Card Repeatable Time: format years=1 '
                                          'or months=2 or days=3 or hours=5 or minutes=6')

            ###

            # card_create = subparsers.add_parser('task')
            # card_create.set_defaults(which='create_task')
            #
            # card_create.add_argument('card_id', action='store',
            #                          help='Card ID where to create task')
            #
            # card_create.add_argument('task_title', action='store',
            #                          help='Task title')
            #
            # card_create.add_argument('--task_description', action='store',
            #                          help='Task description')
            #
            # card_create.add_argument('--task_completed', action="store",
            #                          help='Task completed: True or False')

            ###

            subtask_create = subparsers.add_parser('subtask')
            subtask_create.set_defaults(which='create_subtask')

            subtask_create.add_argument('task_id', action='store',
                                        help='Task ID where to update subtask')

            subtask_create.add_argument('subtask_title', action='store',
                                        help='Subtask title')

            subtask_create.add_argument('--subtask_description', action='store',
                                        help='Subtask description')

            subtask_create.add_argument('--subtask_completed', action="store",
                                        help='Subtask completed: True or False')

            #####################

            subparsers = update_group.add_subparsers()

            board_update = subparsers.add_parser('board')
            board_update.set_defaults(which='update_board')
            board_update.add_argument('board_id', action='store',
                                      help='Board Id')

            board_update.add_argument('--board_title', action='store',
                                      help='Board title')

            board_update.add_argument('--board_description', action='store',
                                      help='Board description')

            ###

            cardlist_update = subparsers.add_parser('cardlist')
            cardlist_update.set_defaults(which='update_cardlist')

            cardlist_update.add_argument('cardlist_id', action='store',
                                         help='Cardlist ID')

            cardlist_update.add_argument('--cardlist_title', action='store',
                                         help='Cardlist title')

            cardlist_update.add_argument('--cardlist_description', action='store',
                                         help='Cardlist description')

            ###

            card_update = subparsers.add_parser('card')
            card_update.set_defaults(which='update_card')

            card_update.add_argument('card_id', action='store',
                                     help='Card ID')

            card_update.add_argument('--card_title', action='store',
                                     help='Card title')

            card_update.add_argument('--card_description', action='store',
                                     help='Card description')

            card_update.add_argument('--card_deadline', action="store",
                                     help='Card deadlile: format %%Y/%%m/%%d-%%H:%%M or %%Y/%%m/%%d')

            card_update.add_argument('--card_repeatable_time', action="store",
                                     help='Card Repeatable Time: format years=1 '
                                          'or months=2 or days=3 or hours=5 or minutes=6')

            card_update.add_argument('--task_completed', action="store",
                                     help='Task completed: True or False')

            ###

            subtask_update = subparsers.add_parser('subtask')
            subtask_update.set_defaults(which='update_subtask')

            subtask_update.add_argument('subtask_id', action='store',
                                        help='Subtask ID')

            subtask_update.add_argument('--subtask_title', action='store',
                                        help='Subtask title')

            subtask_update.add_argument('--subtask_description', action='store',
                                        help='Subtask description')

            subtask_update.add_argument('--subtask_completed', action="store",
                                        help='Subtask completed: True or False')

            #####################

            subparsers = remove_group.add_subparsers()

            board_remove = subparsers.add_parser('board')
            board_remove.set_defaults(which='remove_board')
            board_remove.add_argument('board_id', action="store",
                                      help='remove board: board id')

            cardlist_remove = subparsers.add_parser('cardlist')
            cardlist_remove.set_defaults(which='remove_cardlist')
            cardlist_remove.add_argument('cardlist_id', action="store",
                                         help='remove cardlist info: cardlist id')

            card_remove = subparsers.add_parser('card')
            card_remove.set_defaults(which='remove_card')
            card_remove.add_argument('card_id', action="store",
                                     help='remove card info: card id')

            subtask_remove = subparsers.add_parser('subtask')
            subtask_remove.set_defaults(which='remove_subtask')
            subtask_remove.add_argument('subtask_id', action="store",
                                        help='remove subtask: subtask id')

            ###

            args = vars(parser.parse_args())

            #####################

            if args['which'] == 'show_user':
                if args['current_user']:
                    self._show_curren_user()

            if args['which'] == 'show_user_teams':
                if args['current_user_teams']:
                    self._show_current_user_teams()

            if args['which'] == 'show_board':
                if args['board_id']:
                    self._show_board(args['board_id'])

            if args['which'] == 'show_cardlist':
                if args['cardlist_id']:
                    self._show_cardlist(args['cardlist_id'])

            if args['which'] == 'show_card':
                if args['card_id']:
                    self._show_card(args['card_id'])

            if args['which'] == 'show_task':
                if args['task_id']:
                    self._show_task(args['task_id'])

            if args['which'] == 'show_subtask':
                if args['subtask_id']:
                    self._show_subtask(args['show_subtask'])

            #####################

            if args['which'] == 'create_board':
                board_title = args['board_title']
                board_id = args['team_id']
                board_description = args['board_description']

                if board_id is not None:
                    self._create_team_board(team_id=board_id,
                                            title=board_title, description=board_description)

                else:
                    self._create_board(title=board_title, description=board_description)

            if args['which'] == 'create_cardlist':
                board_id = args['board_id']
                cardlist_title = args['cardlist_title']
                cardlist_description = args['cardlist_description']

                self._create_cardlist(board_id=board_id,
                                      title=cardlist_title, description=cardlist_description)

            if args['which'] == 'create_card':
                cardlist_id = args['cardlist_id']
                cardlist_title = args['card_title']
                cardlist_description = args['card_description']
                card_deadline = args['card_deadline']
                card_repeatable_time = args['card_repeatable_time']

                self._create_card(cardlist_id=cardlist_id,
                                  title=cardlist_title, description=cardlist_description,
                                  deadline=card_deadline, repeatable_time=card_repeatable_time)

            if args['which'] == 'create_subtask':
                task_id = args['task_id']
                subtask_title = args['subtask_title']
                subtask_description = args['subtask_description']

                self._create_subtask(task_id=task_id,
                                     title=subtask_title, description=subtask_description)

            #####################

            if args['which'] == 'update_board':
                board_title = args['board_title']
                board_id = args['board_id']
                board_description = args['board_description']

                self._update_board(board_id=board_id,
                                   title=board_title, description=board_description)

            if args['which'] == 'update_cardlist':
                cardlist_id = args['cardlist_id']
                cardlist_title = args['cardlist_title']
                cardlist_description = args['cardlist_description']

                self._update_cardlist(cardlist_id=cardlist_id,
                                      title=cardlist_title, description=cardlist_description)

            print(args)
            if args['which'] == 'update_card':
                card_id = args['card_id']
                card_title = args['card_title']
                card_description = args['card_description']
                card_deadline = args['card_deadline']
                card_repeatable_time = args['card_repeatable_time']
                task_completed = args['task_completed']

                self._update_card(card_id=card_id,
                                  title=card_title, description=card_description,
                                  deadline=card_deadline, repeatable_time=card_repeatable_time,
                                  completed=task_completed)

            if args['which'] == 'update_subtask':
                subtask_id = args['subtask_id']
                subtask_title = args['subtask_title']
                subtask_description = args['subtask_description']
                subtask_completed = args['subtask_completed']

                self._update_subtask(subtask_id=subtask_id,
                                     title=subtask_title, description=subtask_description,
                                     completed=subtask_completed)

            #####################

            if args['which'] == 'remove_board':
                self._remove_board(args['board_id'])

            if args['which'] == 'remove_cardlist':
                print(args)
                self._remove_cardlist(args['cardlist_id'])

            if args['which'] == 'remove_card':
                self._remove_card(args['card_id'])

            if args['which'] == 'remove_subtask':
                self._remove_subtask(args['subtask_id'])

            #####################

            data = jsonpickle.encode(self.client)
            with open('client.json', 'w') as outfile:
                json.dump(data, outfile)

        except Exception:
            print("Something strange happened")

    #####################

    def _get_board(self, board_id):
        return self.current_user.find_board(board_id=board_id)

    def _get_cardlist(self, cardlist_id):
        for board in self.current_user.user_boards:
            return board.find_cardlist(cardlist_id=cardlist_id)

    def _ger_card(self, card_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:

                card = cardlist.find_card(card_id=card_id)
                if card is not None:
                    return card

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

                    subtask = card.task.find_subtask(subtask_id=subtask_id)
                    if subtask is not None:
                        return subtask

    ###

    def _show_curren_user(self):
        print(self.current_user)

    def _show_current_user_teams(self):
        for team in self.current_user_teams:
            print(team)

    def _show_board(self, board_id):
        board = self._get_board(board_id)
        if board is not None:
            print(board)

    def _show_cardlist(self, cardlist_id):
        cardlist = self._get_cardlist(cardlist_id)
        if cardlist is not None:
            print(cardlist)

    def _show_card(self, card_id):
        card = self._ger_card(card_id)
        if card is not None:
            print(card)

    def _show_task(self, task_id):
        task = self._get_task(task_id)
        if task is not None:
            print(task)

    def _show_subtask(self, subtask_id):
        subtask = self._get_subtask(subtask_id)
        if subtask is not None:
            print(subtask)

    ###

    def _create_board(self, title, description):
        board = scrumban_board.Board(title=title, users_login=self.current_user.id, description=description)
        self.current_user.add_board(board)

    def _create_team_board(self, team_id, title, description):
        for team in self.current_user_teams:
            if team.id == team_id:
                team_members_login = [login for login in team.team_members_login]
                board = scrumban_board.Board(users_login=team_members_login,
                                             title=title, description=description)

                team.add_team_board(board)

    def _create_cardlist(self, title, board_id, description=None):
        board = self._get_board(board_id=board_id)

        if board is not None:
            cardlist = scrumban_board.CardList(title=title, description=description)
            board.add_cardlist(cardlist)

    def _create_card(self, title, cardlist_id, description=None, deadline=None,
                     repeatable_time=None):
        cardlist = self._get_cardlist(cardlist_id)

        if cardlist_id is not None:
            task = scrumban_board.Task(title=title, description=description)

            deadline = scrumban_board.Remind(title=title, when_remind=deadline,
                                             repeatable_time=repeatable_time)

            card = scrumban_board.Card(task=task, users_login=self.current_user.id, deadline=deadline)
            cardlist.add_card(card)

    def _create_subtask(self, title, task_id, description=None):
        task = self._get_task(task_id)

        if task is not None:
            task.add_subtask(scrumban_board.Subtask(title=title, description=description))

    ###

    def _update_board(self, board_id, title=None, description=None):
        board = self._get_board(board_id=board_id)

        board.update_board(title=title, description=description)

    def _update_cardlist(self, cardlist_id, title=None, description=None):
        cardlist = self._get_cardlist(cardlist_id=cardlist_id)

        cardlist.update_cardlist(title=title, description=description)

    def _update_card(self, card_id, title=None, description=None, deadline=None, repeatable_time=None, completed=None):
        card = self._ger_card(card_id=card_id)

        if completed is None:
            card.task.update_task(title=title, description=description)

        else:
            card.task.update_task(title=title, description=description, completed=completed)

        card.update_card(deadline=deadline, reminds_list=repeatable_time)

    def _update_task(self, task_id, title=None, description=None, completed=None):
        task = self._get_task(task_id=task_id)

        if completed is None:
            completed = False

        task.update_task(title=title, description=description, completed=completed)

    def _update_subtask(self, subtask_id, title=None, description=None, completed=None):
        subtask = self._get_subtask(subtask_id=subtask_id)

        if completed is None:
            completed = False

        subtask.update_subtask(title=title, description=description, completed=completed)

    ###

    def _remove_board(self, board_id):
        self.current_user.remove_board(board_id=board_id)

    def _remove_cardlist(self, cardlist_id):
        for board in self.current_user.user_boards:
            if board.find_cardlist(cardlist_id=cardlist_id):
                board.remove_cardlist(cardlist_id=cardlist_id)

    def _remove_card(self, card_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                if cardlist.find_card(card_id=card_id):
                    cardlist.remove_card(card_id=card_id)

    def _remove_subtask(self, subtask_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                for card in cardlist.cards:
                    if card.task.find_subtask(subtask_id=subtask_id):
                        card.task.remove_subtask(subtask_id=subtask_id)

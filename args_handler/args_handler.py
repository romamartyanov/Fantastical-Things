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

        parser = argparse.ArgumentParser()

        parser.add_argument('--show_current_user', action='store_true',
                            help='Show Current user')

        parser.add_argument('--show_current_user_teams', action='store_true',
                            help='Show Current user')

        parser.add_argument('--show_board', action="store",
                            help='Show Board in current user: board id')

        parser.add_argument('--show_cardlist', action="store",
                            help='Show Cardlist in current user: cardlist id')

        parser.add_argument('--show_card', action="store",
                            help='Show Card in current user: card id')

        parser.add_argument('--show_task', action="store",
                            help='Show Task in current user: task id')

        parser.add_argument('--show_remind', action="store",
                            help='Show Remind in current user: remind id')

        parser.add_argument('--show_subtask', action="store",
                            help='Show Subask in current user: subtask id')

    ###

        parser.add_argument('--create_subtask_where', action="store",
                            help='Create Subtask: task id')

        parser.add_argument('--subtask_title', action="store",
                            help='An optional integer argument')

        parser.add_argument('--subtask_description', action="store",
                            help='An optional integer argument')

        parser.add_argument('--subtask_completed', action="store",
                            help='An optional integer argument')

    ###

        parser.add_argument('--create_task_where', action="store",
                            help='Create Task: card id')

        parser.add_argument('--task_title', action="store",
                            help='An optional integer argument')

        parser.add_argument('--task_description', action="store",
                            help='An optional integer argument')

        parser.add_argument('--task_completed', action="store",
                            help='An optional integer argument')

    ###

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


###

    def show_curren_user(self):
        print(self.current_user)

    def show_current_user_teams(self):
        for team in self.current_user_teams:
            print(team)

    def show_board(self, board_id):
        board = self.current_user.find_board(board_id=board_id)
        if board is not None:
            print(board)

        return

    def show_cardlist(self, cardlist_id):
        for board in self.current_user.user_boards:
            cardlist = board.find_cardlist(cardlist_id=cardlist_id)

            if cardlist is not None:
                print(cardlist)

                return

    def show_card(self, card_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                card = cardlist.find_card(card_id=card_id)

                if card is not None:
                    print(card)

                    return

    def show_task(self, task_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                for card in cardlist.cards:
                    if card.task.id == task_id:
                        print(card.task)

                        return

    def show_subtask(self, subtask_id):
        for board in self.current_user.user_boards:
            for cardlist in board.cardlists:
                for card in cardlist.cards:
                    subtask = card.task.find_subtask(subtask_id=subtask_id)
                    if subtask is not None:
                        print(subtask)

                        return

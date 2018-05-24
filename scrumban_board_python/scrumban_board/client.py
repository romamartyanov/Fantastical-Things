import configparser
import os
from datetime import *

from scrumban_board_python.scrumban_board.client_users import ClientUsers
from scrumban_board_python.scrumban_board.client_teams import ClientTeams


class Client:
    def __init__(self,
                 client_users: ClientUsers = None, client_teams: ClientTeams = None):

        self.client_users = ClientUsers()
        self.client_teams = ClientTeams()

        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'current_user.cfg'))

        self.current_user_login = config["USER"]["UserLogin"]

        if client_users is not None:
            self.client_users = client_users

        if client_teams is not None:
            self.client_teams = client_teams

    def update_all_reminds(self):
        # going throw all users
        for user in self.client_users.users:

            # going throw all user boards
            for board in user.user_boards:
                overdue_cardlist = board.find_cardlist(title="Overdue")

                for cardlist in board.cardlists:

                    # if cardlist is for overdue cards
                    if cardlist.title == "Overdue":
                        continue

                    for card in cardlist.cards:

                        # check deadline:
                        if card.deadline is not None:
                            if card.deadline.when_remind > datetime.now():

                                # print card with this deadline
                                for user_login in card.users_login:
                                    if user_login == self.current_user_login:
                                        print(card)

                                # card is repeatable
                                if card.deadline.repeating_remind_relativedelta is not None:
                                    card.deadline.when_remind += card.deadline.repeating_remind_relativedelta

                                # card is not repeatable
                                else:
                                    # may be it will not work
                                    board.move_card(card.id, cardlist.id, overdue_cardlist.id)

                        # check all reminds in the card
                        for remind in card.reminds_list:

                            # if we need to remind about card
                            if remind.when_remind > datetime.now():

                                # print card with this remind
                                for user_login in card.users_login:
                                    if user_login == self.current_user_login:
                                        print(card)

                                if remind.is_repeatable:
                                    remind.when_remind += remind.repeating_remind_relativedelta

                                else:
                                    card.remove_remind(remind)

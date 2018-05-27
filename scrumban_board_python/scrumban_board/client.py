import configparser
import logging.config

from datetime import *

from scrumban_board_python.scrumban_board.client_users import ClientUsers
from scrumban_board_python.scrumban_board.client_teams import ClientTeams

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("ScrumbanBoard")


class Client:
    """
    Client is the class responsible for the entire library,
    because it is the accumulator of all other classes of the library.

    Example:

    client = scrumban_board.Client()
    user = scrumban_board.User("Roman", "Martyanov", "romamartyanov", "romamartyanov@gmail.com")
    client.client_users.add_new_user(user)

    while not client.update_all_reminds():
        continue
    """

    def __init__(self, config_file_path: str,
                 client_users: ClientUsers = None, client_teams: ClientTeams = None):
        """
        Initialising of Client

        :param client_users: all Users
        :param client_teams: all Teams
        """

        config = configparser.ConfigParser()
        config.read(config_file_path)

        self.current_user_login = config["USER"]["UserLogin"]
        self.client_data_path = config["CLIENT"]["DataPath"]

        self.client_users = ClientUsers()
        self.client_teams = ClientTeams()

        if client_users is not None:
            self.client_users = client_users

        if client_teams is not None:
            self.client_teams = client_teams

        logger.info("Client was created")

    def _check_deadline(self, board, overdue_cardlist, cardlist, card):
        if card.deadline.when_remind < datetime.now():

            if card.deadline.repeating_remind_relativedelta is not None:

                card.deadline.when_remind += card.deadline.repeating_remind_relativedelta
                logger.info("Deadline in card ({}) was delayed".format(card.id))

                for user_login in card.users_login:
                    if user_login == self.current_user_login:
                        print(card)

            else:
                board.move_card(card.id, cardlist.id, overdue_cardlist.id)

                print(board)

                logger.info(
                    "Card ({}) was moved to the Overdue Cardlist ({}) in the Board ({})".format(
                        card.id,
                        cardlist.id,
                        board.id))

                for user_login in card.users_login:
                    if user_login == self.current_user_login:
                        print(card)

                return False

        return True

    def _check_remind(self, board, cardlist, card, remind):
        if remind.when_remind < datetime.now():

            logger.info(
                "Remind about Card ({}) in the Cardlist ({}) on the Board ({})".format(card.id,
                                                                                       cardlist.id,
                                                                                       board.id))

            for user_login in card.users_login:
                if user_login == self.current_user_login:
                    print(card)

            if remind.is_repeatable:
                remind.when_remind += remind.repeating_remind_relativedelta

                logger.info(
                    "Remind ({}) was delayed in the "
                    "Card ({}) in the Cardlist ({}) on the Board ({})".format(remind.id,
                                                                              card.id,
                                                                              cardlist.id,
                                                                              board.id))

            else:
                card.remove_remind(remind)

                logger.info(
                    "Remind ({}) was removed in the "
                    "Card ({}) in the Cardlist ({}) on the Board ({})".format(remind.id,
                                                                              card.id,
                                                                              cardlist.id,
                                                                              board.id))

            for user_login in card.users_login:
                if user_login == self.current_user_login:
                    print(card)

            return False

    def _check_card(self, board, overdue_cardlist, cardlist, card):
        if card.deadline is not None:
            if not self._check_deadline(board, overdue_cardlist, cardlist, card):
                return False

        for remind in card.reminds_list:
            # if not self.check_remind(board, cardlist, card, remind):
            #   return False
            pass

        return True

    def _check_cardlist(self, board, overdue_cardlist, cardlist):
        if cardlist.title == "Overdue":
            return True

        for card in cardlist.cards:
            if not self._check_card(board, overdue_cardlist, cardlist, card):
                return False

        return True

    def _check_board(self, board):
        overdue_cardlist = board.find_cardlist(cardlist_title="Overdue")

        for cardlist in board.cardlists:
            if not self._check_cardlist(board, overdue_cardlist, cardlist):
                print(board)

                return False

        return True

    def _updating_users(self):
        for user in self.client_users.users:

            for board in user.user_boards:
                if not self._check_board(board):
                    return False

        return True

    def _updating_teams(self):
        for team in self.client_teams.teams:

            for board in team.team_boards:
                if not self._check_board(board):
                    return False

        return True

    def update_all_reminds(self):
        """Updating all reminds in the Client"""

        if not self._updating_users():
            return False

        if not self._updating_teams():
            return False

        return True

import configparser
import os
import logging.config

from datetime import *

from scrumban_board_python.scrumban_board.client_users import ClientUsers
from scrumban_board_python.scrumban_board.client_teams import ClientTeams

# creating logger for client
logging.config.fileConfig(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logging.cfg'))

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

        # reading client configurations
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

    def update_all_reminds(self):
        """Updating all reminds in the Client"""

        # going through all users
        for user in self.client_users.users:

            # going throw all user boards
            for board in user.user_boards:
                overdue_cardlist = board.find_cardlist(cardlist_title="Overdue")

                for cardlist in board.cardlists:

                    # if cardlist is for overdue cards
                    if cardlist.title == "Overdue":
                        continue

                    for card in cardlist.cards:

                        # check deadline:
                        if card.deadline is not None:
                            if card.deadline.when_remind < datetime.now():

                                # card is repeatable
                                if card.deadline.repeating_remind_relativedelta is not None:

                                    logger.info("Deadline in card ({}) was delayed".format(card.id))

                                    for user_login in card.users_login:
                                        if user_login == self.current_user_login:
                                            print(card)

                                # card is not repeatable
                                else:
                                    # may be it will not work
                                    board.move_card(card.id, cardlist.id, overdue_cardlist.id)

                                    logger.info(
                                        "Card ({}) was moved to the Overdue Cardlist ({}) in the Board ({})".format(
                                            card.id,
                                            cardlist.id,
                                            board.id))

                                    for user_login in card.users_login:
                                        if user_login == self.current_user_login:
                                            print(card)

                                    return False

                        # check all reminds in the card
                        for remind in card.reminds_list:

                            # if we need to remind about card
                            if remind.when_remind < datetime.now():

                                logger.info(
                                    "Remind about Card ({}) in the Cardlist ({}) on the Board ({})".format(card.id,
                                                                                                           cardlist.id,
                                                                                                           board.id))

                                # print card with this remind
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

                                # print card with this remind
                                for user_login in card.users_login:
                                    if user_login == self.current_user_login:
                                        print(card)

                                return False

        return True

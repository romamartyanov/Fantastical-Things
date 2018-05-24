import configparser
import os

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
        pass

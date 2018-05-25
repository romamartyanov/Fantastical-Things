from collections import deque

from scrumban_board_python.scrumban_board.team import Team


class ClientTeams:
    """
    ClientTeams in the class responsible for storing all the Teams of the Client

    Example:

    team = scrumban_board.Team(client.logger, "200 OK", "200_OK", "romamartyanov")
    client.client_teams.add_new_team(team)
    """

    def __init__(self, logger, teams: deque = None):
        """
        Initialising of ClientTeams

        :param logger: client logger
        :param teams: Teams for the storage
        """
        self.teams = deque()

        if teams is not None:
            for team in teams:
                if isinstance(team, Team):
                    self.teams.append(team)

        self._logger = logger
        self._logger.info("ClientTeams was created")

    def update_client_teams(self, teams: deque):
        """
        Updating object fields with new data

        :param teams: new Teams for the storage
        :return:
        """
        self.teams.clear()

        for team in teams:
            if isinstance(team, Team):
                if isinstance(team, Team):
                    self.teams.append(team)

        self._logger.info("ClientTeams was updated")

    def find_team(self, team_id: str = None, team_login: str = None):
        """
        Searching Team

        :param team_id: team_id for searching
        :param team_login: team_login for searching
        :return: Team - if was found; None - if wasn't found
        """
        if team_id is not None:
            try:
                team = next(team for team in self.teams if team.login == team_id)
                self._logger.info("Team was found by team_id ({})".format(team_id))

                return team

            except StopIteration:
                self._logger.info("Team wasn't found by team_id ({})".format(team_id))

        elif team_login is not None:
            try:
                team = next(team for team in self.teams if team.nickname == team_login)
                self._logger.info("Team was found by team_login ({})".format(team_login))

                return team

            except StopIteration:
                self._logger.info("Team wasn't found by team_login ({})".format(team_login))

        return None

    def add_new_team(self, team: Team):
        """
        Adding new Team to self.teams

        :param team: new Team
        :return:
        """
        duplacate_team = self.find_team(team.login)

        if duplacate_team is None:
            self.teams.append(team)
            self._logger.info("new Team ({}) was added".format(team.id))

    def remove_team(self, team):
        """

        :param team: Team or Team.id
        :return:
        """
        if isinstance(team, Team):
            duplacate_team = self.find_team(team_login=team.login)

            if duplacate_team is not None:
                self.teams.remove(duplacate_team)
                self._logger.info("Team ({}) was removed".format(duplacate_team.id))

        elif isinstance(team, str):
            duplacate_team_login = self.find_team(team_login=team)
            duplacate_team_id = self.find_team(team_id=team)

            if duplacate_team_login is not None:
                self.teams.remove(duplacate_team_login)
                self._logger.info("Team ({}) was removed".format(duplacate_team_login.id))

            if duplacate_team_id is not None:
                self.teams.remove(duplacate_team_id)
                self._logger.info("Team ({}) was removed".format(duplacate_team_login.id))

from collections import deque

from scrumban_board_python.scrumban_board.team import Team


class ClientTeams:
    def __init__(self, teams: deque = None):
        self.teams = deque()

        if teams is not None:
            for team in teams:
                if isinstance(team, Team):
                    self.teams.append(team)

    def update_client_teams(self, teams: deque):
        self.teams.clear()

        for team in teams:
            if isinstance(team, Team):
                if isinstance(team, Team):
                    self.teams.append(team)

    def find_team(self, team_id: str = None, team_login: str = None):
        if team_id is not None:
            try:
                return next(team for team in self.teams if team.login == team_id)

            except StopIteration:
                return None

        elif team_login is not None:
            try:
                return next(team for team in self.teams if team.nickname == team_login)

            except StopIteration:
                return None

    def add_new_team(self, team: Team):
        duplacate_team = self.find_team(team.login)

        if duplacate_team is None:
            self.teams.append(team)

    def remove_team(self, team):
        if isinstance(team, Team):
            duplacate_team = self.find_team(team_login=team.login)

            if duplacate_team is not None:
                self.teams.remove(duplacate_team)

        elif isinstance(team, str):
            duplacate_team_login = self.find_team(team_login=team)

            if duplacate_team_login is not None:
                self.teams.remove(duplacate_team_login)


class League:
    """_summary_
    """
    def __init__(self, league_name, league_id):
        self.seasons = {}
        self.league_name = league_name
        self.id = league_id
    def get_season(self, year):
        """_summary_

        Args:
            year (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.seasons[year]
    def update_season(self, season):
        """_summary_

        Args:
            season (_type_): _description_
        """
        
        self.seasons[season.year] = season
    def get_team(self, id, year = None):
        """_summary_

        Args:
            id (_type_): _description_
            year (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if year is not None and self.seasons[year]:
            if id in self.seasons[year].teams:
                return dict(self.seasons[year].teams[id])
            else:
                print(f"Team with {id} in year {year} does not exist")
        elif year is None:
            team_seasons = dict()
            for season in self.seasons:
                if season.teams[id]:
                    team_seasons[season.id] = season.teams[id]
            return team_seasons
        else:
            print(f"Team with {id} was not found in any league")
class Game:
    def __init__(self, week, name, id, score, opponent_id, opponent_name, opponent_score):
        self.week = week
        self.score = score
        self.opponent_id = opponent_id
        self.opponent_score = opponent_score
        self.opponent_name = opponent_name
        self.name = name
        self.id = id
class Team:
    """_summary_
    """
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.owner=""
        self.championships = {}
        self.total_points = 0
        self.total_points_against = 0
        self.wins = 0
        self.losses = 0
        self.rank = 0
        self.ties = 0
        self.division = ""
        self.games = dict()
        
    def add_ship(self, championship):
        """_summary_

        Args:
            championship (_type_): _description_
        """
        self.championships[championship.year] = championship
    def add_total_points(self, points):
        """_summary_

        Args:
            points (_type_): _description_
        """
        self.total_points = points
    def add_game(self, game):
        """Add a game to a team

        Args:
            game (_type_): _description_
        """
        self.games[game.week] = game
        
    def add_record(self, win_loss_tie, total_point, total_points_against, division=""):
        """_summary_

        Args:
            win_loss_ tie (_type_): _description_
        """
        wlt = win_loss_tie.split('-')
        self.wins = wlt[0]
        self.losses = wlt[1]
        self.ties = wlt[2]
        self.total_points = total_point
        self.total_points_against = total_points_against
        self.division = division
    def add_rank(self, rank):
        """_summary_

        Args:
            rank (_type_): _description_
        """
        self.rank = rank
        
class Season:
    """_summary_
    """
    def __init__(self, year, team):
        self.year = year
        self.teams = dict()
        self.teams[team.id]=team
        self.highest_score = 0
        self.highest_score_team_id = 0
        self.highest_score_week = 0
        self.points_leader_total = 0
        self.points_leader_team_id = 0
        self.highest_player_team_id = 0
        self.highest_player_points = 0
        self.highest_player_week = 0
        self.highest_player_name = ""
        self.highest_player_pos_team = ""
        self.playoffs = []
    def add_team(self, team):
        """_summary_

        Args:
            team (_type_): _description_
        """
        self.teams[team.id]=team
    def add_playoff_game(self, game):
        self.playoffs.append(game)
        a_team = self.teams[game.id]
        #double check a_team, and b_team don't need to be updated on season
        a_team.add_game(game)
        b_team = self.teams[game.opponent_id]
        game_flipped = Game(game.week, b_team.name, b_team.id, game.opponent_score, a_team.name, a_team.id, a_team.score)
        b_team.add_game(game_flipped)
    def set_highest_score(self, team_id, score, week):
        """_summary_

        Args:
            team (_type_): _description_
            score (_type_): _description_
            week (_type_): _description_
        """
        self.highest_score = score
        self.highest_score_team_id = team_id
        self.highest_score_week = week
    def set_points_leader(self, team_id, points):
        """_summary_

        Args:
            team (_type_): _description_
            points (_type_): _description_
        """
        self.points_leader_total = points
        self.points_leader_team_id = team_id
    def set_highest_player_score(self, team_id, points, week, player_name, pos_team):
        """_summary_

        Args:
            team (_type_): _description_
            points (_type_): _description_
            week (_type_): _description_
            player_name (_type_): _description_
            pos_team (_type_): _description_
        """
        self.highest_player_team_id = team_id
        self.highest_player_points = points
        self.highest_player_week = week
        self.highest_player_name = player_name
        self.highest_player_pos_team = pos_team
class Championship:
    """_summary_
    """
    def __init__(self, year):
        self.year = year
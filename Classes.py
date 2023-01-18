class Player:
    def __init__(self, name, defending,pace,shooting,passing, teamwork, pos ) -> None:
        self.Name = name
        self.Defending = defending
        self.Pace = pace
        self.Shooting = shooting
        self.Passing = passing
        self.Teamwork = teamwork
        self.Position = pos

class Team:
    def __init__(self, name, formation, tactics, players) -> None:
        self.Name = name
        self.Formation = formation
        self.tatcitcs = tactics
        self.players = players

class Ref:
    def __init__(self, patience, truth) -> None:
        self.patience =  patience
        self.truth = truth
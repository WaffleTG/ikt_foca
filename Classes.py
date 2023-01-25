class Player:
    def __init__(self, name, defending,pace,attacking,passing, teamwork, pos ) -> None:
        self.Name = name
        self.Stats = {
            "Defending":defending,
            "Pace": pace,
            "Attacking": attacking,
            "Passing": passing,
        }
        # self.Defending = defending
        # self.Pace = pace
        # self.Attacking = attacking
        # self.Passing = passing
        self.Teamwork = teamwork
        self.Position = pos
        self.Overall = int(sum(self.Stats.values()) / 2 + float(max(self.Stats.values())) * 1.5)
        

class Team:
    def __init__(self, name: str, formation: str, tactics: dict,players: dict) -> None:
        self.Name = name
        self.Formation = formation
        self.Tatcitcs = tactics
        self.Players = players
        self.Overall = 0
        self.TeamWorkOverall = 0
        for player in self.Players.values():
            self.Overall += player.Overall
            self.TeamWorkOverall += player.Teamwork
        self.Overall *= (self.TeamWorkOverall/50/len(self.Players))
        
        

class Ref:
    def __init__(self, patience, truth) -> None:
        self.patience =  patience
        self.truth = truth
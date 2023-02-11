class Player:
    def __init__(self, name: str, defending: int,pace: int,attacking: int,passing: int, goalkeepeing: int, teamwork: int, pos: str) -> None:
        self.Name = name
        self.Stats = {
            "Defending":defending,
            "Pace": pace,
            "Attacking": attacking,
            "Passing": passing,
            "GoalKeeping": goalkeepeing,
            "Teamwork": teamwork
        }
        # self.Defending = defending
        # self.Pace = pace
        # self.Attacking = attacking
        # self.Passing = passing
        # self.Teamwork = teamwork
        self.Position = pos
        self.Overall = int((sum(self.Stats.values()) / 2 + float(max(self.Stats.values())) * 1.5)/4.5)
        print(self.Overall)

class Team:
    def __init__(self, name: str, formation: str, tactics: dict,players: dict) -> None:
        self.Name = name
        self.Formation = formation
        self.Tactics = tactics
        self.Players = players
        self.Overall = 0
        self.TeamWorkOverall = 0
        self.AttOverall = 0
        self.MidOverall = 0
        self.DefOverall = 0
        self.KeeperOverall = 0
        
    def getTeamWork(self):
        if len(self.Players) > 0:
            ovr = 0
            for player in self.Players.values():
                ovr += player.Stats["Teamwork"]
            self.TeamWorkOverall = ovr/len(self.Players)
            
        else:
            self.TeamWorkOverall = 0
        return self.TeamWorkOverall
    def getOverall(self):
        pass

class Ref:
    def __init__(self, patience, truth) -> None:
        self.patience =  patience
        self.truth = truth
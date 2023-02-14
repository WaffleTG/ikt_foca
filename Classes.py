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

    def SetStats(self, debug=False):
        self.DefOverall = 0
        self.KeeperOverall = 0
        self.AttOverall = 0
        self.MidOverall = 0
        try:
            self.KeeperOverall = self.Players["GK"].Stats["GoalKeeping"] * self.getTeamWork() / 99
        except KeyError:
            #Team Doesn't have a keeper (probably need a messagebox)
            pass
        for key, player in self.Players.items():
            if "B" in key:
                self.DefOverall += player.Overall*self.TeamWorkOverall/50/4
            elif "M" in key:
                self.MidOverall += player.Overall*self.TeamWorkOverall/50/3
            elif "W" in key or "T" in key:
                self.AttOverall += player.Overall*self.TeamWorkOverall/50/3
        if debug:
            print(f"AttOveral{self.AttOverall}")
        if debug:
            print(f"Teamname: {self.Name} Attack Overall: {self.AttOverall} Midfield Overall: {self.MidOverall} Defense Overall: {self.DefOverall} Keeper Overall: {self.KeeperOverall} Teamwork Overall: {self.getTeamWork()}")

class Chance:
    def __init__(self, time, team: int, goal=False) -> None:
        self.Time = time
        self.Team = team
        self.Comm = ""
        self.IsGoal = goal
class Ref:
    def __init__(self, patience, truth) -> None:
        self.patience =  patience
        self.truth = truth
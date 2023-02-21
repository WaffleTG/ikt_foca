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
        defOvr = 0
        midOvr = 0
        attOvr = 0
        keepOvr = 0

        try:
            keepOvr += self.Players["GK"].Stats["GoalKeeping"] * self.getTeamWork() / 99
        except KeyError:
            #Team Doesn't have a keeper (probably need a messagebox)
            pass
        for key, player in self.Players.items():
            if "B" in key:
                print(player.Overall)
                defOvr += player.Overall*self.getTeamWork()/50/4
            elif "M" in key:
                midOvr += player.Overall*self.getTeamWork()/50/3
                print(player.Overall)
            elif "W" in key or "T" in key:
                print(player.Overall)
                attOvr += player.Overall*self.getTeamWork()/50/3
        self.MidOverall = midOvr
        self.DefOverall = defOvr
        self.AttOverall = attOvr
        self.KeeperOverall = keepOvr
        if debug:
            print(f"Teamname: {self.Name} Attack Overall: {self.AttOverall} Midfield Overall: {self.MidOverall} Defense Overall: {self.DefOverall} Keeper Overall: {self.KeeperOverall} Teamwork Overall: {self.getTeamWork()}")
        

class Chance:
    def __init__(self, time, team: int, chanceType:str, player:Player) -> None:
        self.Time = time
        self.Team = team
        self.Comm = "Kindian"
        self.ChanceType = chanceType
        self.Player = player
    def GenerateComm(self):
        pass
class Ref:
    def __init__(self, patience, truth) -> None:
        self.patience =  patience
        self.truth = truth
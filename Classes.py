from Data import Commentaries
import random

class Player:
    def __init__(self, name: str, defending: int,pace: int,attacking: int,passing: int, goalkeepeing: int, teamwork: int, stamina: int, agressivness: int, pos: str ) -> None:
        self.Name = name
        self.Stats = {
            "Defending":defending,
            "Pace": pace,
            "Attacking": attacking,
            "Passing": passing,
            "GoalKeeping": goalkeepeing,
            "Teamwork": teamwork,
            "Stamina": stamina,
            "Agressivness": agressivness
        }
        # self.Defending = defending
        # self.Pace = pace
        # self.Attacking = attacking
        # self.Passing = passing
        # self.Teamwork = teamwork
        self.Position = pos
        self.Overall = int((sum(self.Stats.values()) / 2 + float(max(self.Stats.values())) * 1.5)/5.5)
        self.YellowCards = 0
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
        self.ActivePlayers = {}
        self.SimulationId = 0
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
    def GetActivePlayers(self):
        activePlayers = {key:player for key,player in self.Players.items() if "SUB" not in key and "RES" not in key}
        self.ActivePlayers = activePlayers.copy()

    def SetStats(self,SimId: int ,debug=False):
        defOvr = 0
        midOvr = 0
        attOvr = 0
        keepOvr = 0
        self.SimulationId = SimId
        self.GetActivePlayers()
        try:
            keepOvr += self.Players["GK"].Stats["GoalKeeping"] * self.getTeamWork() / 99
        except KeyError:
            #Team Doesn't have a keeper (probably need a messagebox)
            pass
        for key, player in self.ActivePlayers.items():
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
    def __init__(self, time, team: Team, chanceType:str, player:Player) -> None:
        self.Time = time
        self.Team = team
        self.Comm = "Commentary Not Set"
        self.ChanceType = chanceType
        self.Player = player
    def GenerateComm(self):
        self.Team.GetActivePlayers()
        self.Comm = random.choice(Commentaries[self.ChanceType]).replace("$NEV", self.Player.Name.split()[0]).replace("$IDO", str(self.Time)).replace("$CSAPATNEV", self.Team.Name).replace("$RANDPLAYER", random.choice(list(self.Team.ActivePlayers.values())).Name).replace("$RAND", str(random.randint(1,200)))
        
class Ref:
    def __init__(self, patience, mistakes, name) -> None:
        self.Name = name
        self.Patience =  patience
        self.Mistakes = mistakes
# print(Commentaries.keys())
# Chance1 = Chance(1, Team("asdasd", "4-4-2", {}, {"LM":  Player("kindina", 1, 2,3,4,5,6,7,8,"a")}), "Goal", Player("d", 1, 2,3,4,5,6,7,8,"a"))
# Chance1.GenerateComm()
# print(Chance1.Comm)
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
        self.Fitness = 100
        # self.Defending = defending
        # self.Pace = pace
        # self.Attacking = attacking
        # self.Passing = passing
        # self.Teamwork = teamwork
        self.Position = pos
        self.SetOverall()
        self.YellowCards = 0
        self.Goals = 0
    def SetOverall(self):
        self.Overall = int(((sum(self.Stats.values()) / 2 + float(max(self.Stats.values())) * 1.5)/550)*abs(self.Fitness))
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
    def getFitnessOverall(self):
        fitness = 0
        self.GetActivePlayers()
        for player in self.ActivePlayers.values():
            fitness += player.Fitness
        return fitness/len(self.ActivePlayers.values())
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
            pass
        for key, player in self.ActivePlayers.items():
            player.SetOverall()
            if "B" in key:
                defOvr += player.Overall*self.getTeamWork()/50/4
            elif "M" in key:
                midOvr += player.Overall*self.getTeamWork()/50/3
            elif "W" in key or "T" in key:
                attOvr += player.Overall*self.getTeamWork()/50/3
            # print(player.Overall)
        self.MidOverall = abs(int(midOvr -self.Tactics["Defwidth"]/20 + self.Tactics["Defline"]/20 + self.Tactics["Agressivness"]/20 + self.Tactics["Defstyle"]/20 + self.Tactics["Attackwidth"]/40 - self.Tactics["Passlength"]/10 - self.Tactics["Attackspeed"]/20 - self.Tactics["Shootrate"]/40))
        self.DefOverall = abs(int(defOvr + self.Tactics["Defwidth"]/20 - self.Tactics["Defline"]/10 + self.Tactics["Agressivness"]/20 - self.Tactics["Defstyle"]/10 + self.Tactics["Passlength"]/10 + self.Tactics["Attackspeed"]/20 - self.Tactics["Shootrate"]/20))
        self.AttOverall = abs(int(attOvr - self.Tactics["Defwidth"]/40 + self.Tactics["Defline"]/20 - self.Tactics["Agressivness"]/40 - self.Tactics["Attackwidth"]/20 - self.Tactics["Passlength"]/10 - self.Tactics["Attackspeed"]/20 + self.Tactics["Shootrate"]/10)) 
        self.KeeperOverall = keepOvr
        if debug:
            print(f"Teamname: {self.Name} Attack Overall: {self.AttOverall} Midfield Overall: {self.MidOverall} Defense Overall: {self.DefOverall} Keeper Overall: {self.KeeperOverall} Teamwork Overall: {self.getTeamWork()}")
        
    def HandleFitness(self, Matchlength:int):
        self.GetActivePlayers()
        for player in self.ActivePlayers.values():
            player.Fitness -= random.uniform(50/Matchlength, 50/Matchlength+(100-player.Stats["Stamina"])/100)
            player.SetOverall()
        self.SetStats(self.SimulationId)
class Chance:
    def __init__(self, time, team: Team, chanceType:str, player:Player) -> None:
        self.Time = time
        self.Team = team
        self.Comm = "Commentary Not Set"
        self.ChanceType = chanceType
        self.Player = player
    def GenerateComm(self):
        self.Team.GetActivePlayers()
        self.Comm = random.choice(Commentaries[self.ChanceType]).replace("$NEV", self.Player.Name.split()[0]).replace("$IDO", str(self.Time)).replace("$CSAPATNEV", self.Team.Name).replace("$RANDPLAYER", random.choice(list(self.Team.ActivePlayers.values())).Name).replace("$RAND", str(random.randint(1,200))).replace("$GOLOKSZAMA", str(self.Player.Goals)).replace("$GOALKEEPERNAME",self.Team.Players.get("GK", random.choice(list(self.Team.Players.values()))).Name)
        
class Ref:
    def __init__(self, patience, mistakes, name) -> None:
        self.Name = name
        self.Patience =  patience
        self.Mistakes = mistakes

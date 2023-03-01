from Classes import Team, Player
from Data import Teams, currentSS, LastTeam, LastTeam, SaveFileRoute, TacticsKeys
import random
from datetime import datetime

def Save(slot:int):
    f = open(f"{SaveFileRoute}save{slot}.save", "w", encoding="utf-8")
    for team in Teams.values():
        line = f"{team.Name};{team.Formation};"
        # f.write(f"{team.Name};{team.Formation};")
        for a in dict(team.Tactics).values():
            line += f"{a},"
            # f.write(f"{a},")
        line = f"{line[:-1]};"
        
        for key, a in dict(team.Players).items():
            stats = ""
            for stat in a.Stats.values():
                stats += f"{stat}:"
            line += f"{a.Name}:{stats}{a.Position}:{key},"
        if len(team.Players) == 0:
            line += ";"
        f.write(f"{line[:-1]}\n")
    
    f.close()
    with open(f"{SaveFileRoute}save{slot}.save", "r", encoding="utf-8") as f:
        print(f.readlines())


def Load(slot:int):
    teams = Teams
    try:
        f = open(f"{SaveFileRoute}save{slot}.save", "r", encoding="utf-8")
        # f.readline()
        for sor in f:
            adatok = sor.strip().split(";")
            tactData = list(map(int, adatok[2].split(",")))
            tact = {key:tactData[i] for i, key in enumerate(TacticsKeys)}
            playerData = adatok[3].split(",")
            players = {}
            for data in playerData:
                OnePlayerData = data.split(":")
                try:
                    player = Player(OnePlayerData[0], int(OnePlayerData[1]), int(OnePlayerData[2]), int(OnePlayerData[3]), int(OnePlayerData[4]), int(OnePlayerData[5]), int(OnePlayerData[6]), int(OnePlayerData[7]), int(OnePlayerData[8]), OnePlayerData[9])
                    players.setdefault(OnePlayerData[10], player)
                
                except IndexError:
                    print("Error")
                    players = {}
            teams[adatok[0]] = Team(adatok[0], adatok[1], tact, players)
        
        f.close()
        currentSS=slot
        return "Sikeres Betöltés"
    except FileNotFoundError:
        f = open(f"{SaveFileRoute}save{slot}.save{slot}", "w", encoding="utf-8")
        f.write(" ")
        f.close()
        currentSS=slot
        return "Új fájl létrehozva"
    except ValueError:
        return "Load Failed"

def SimulateMatch(team1: Team, team2: Team, Chances: int=10, MatchLength: int=90):
    for chance in Chances:
        pass

def FormatPosition(Pos):
    NewPos = ''.join(filter(lambda x: not x.isdigit(), Pos))
    if "ST" in Pos:
        NewPos = "ST"
    return NewPos

def FormatRefereeFileOnstart():
    with open("Datafiles/Referees.txt", "r", encoding="utf-8") as f:
        file = ""
        referees = f.readlines()
        for ref in referees:
            data = ref.strip().split()
            file += f"{data[0]} {data[1]} {random.randint(10,99)} {random.randint(10,99)}\n"
    with open("Datafiles/Referees.txt", "w", encoding="utf-8") as f:
        f.write(file.strip())

def OnStart(Message=""):
    try:
        with open("Datafiles/StartLog.txt", "x", encoding="utf-8") as f:
            f.write("")
        FormatRefereeFileOnstart()

    except FileExistsError:
        with open("Datafiles/StartLog.txt", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            f.write(f"{now}{Message}\n")
def GenerateRandName():
    with open("Datafiles/Referees.txt", "r", encoding="utf-8") as f:
        lines = list(f.readlines())
        return f"{random.choice(lines).strip().split(' ')[random.randint(0,1)]} {random.choice(lines).strip().split(' ')[random.randint(0,1)]}"

def GetTeamIndexByName(teamName: str):
    return list(Teams.keys()).index(teamName)


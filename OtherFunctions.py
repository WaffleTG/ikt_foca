from Classes import Team, Player
from Data import Teams, currentSS, LastTeam, LastTeam

def Save(slot:int):
    f = open(f"save{slot}.save", "w", encoding="utf-8")
    for team in Teams.values():
        line = f"{team.Name};{team.Formation};"
        # f.write(f"{team.Name};{team.Formation};")
        for a in dict(team.Tactics).values():
            line += f"{a},"
            # f.write(f"{a},")
        line = f"{line[:-1]};"
        
        for a in dict(team.Players).values():
            print(a)
            stats = ""
            for stat in a.Stats.values():
                stats += f"{stat}:"
            line += f"{a.Name}:{stats}{a.Position},"
        if len(team.Players) == 0:
            line += ";"
        f.write(f"{line[:-1]}\n")
    
    f.close()
    with open(f"save{slot}.save", "r", encoding="utf-8") as f:
        print(f.readlines())


def Load(slot:int):
    teams = Teams
    try:
        f = open(f"save{slot}.save", "r", encoding="utf-8")
        # f.readline()
        for sor in f:
            adatok = sor.strip().split(";")
            tactData = list(map(int, adatok[2].split(",")))
            tact = {
                "Defwidth": tactData[0],
                "Defline": tactData[1],
                "Agressivness": tactData[2],
                "Defstyle": tactData[3],
                "Attackwidth": tactData[4],
                "Passlength": tactData[5],
                "Attackspeed": tactData[6],
                "Shootrate": tactData[7]
            }
            playerData = adatok[3].split(",")
            players = {}
            for data in playerData:
                OnePlayerData = data.split(":")
                try:
                    player = Player(OnePlayerData[0], int(OnePlayerData[1]), int(OnePlayerData[2]), int(OnePlayerData[3]), int(OnePlayerData[4]), int(OnePlayerData[5]), int(OnePlayerData[6]), OnePlayerData[7])
                    players.setdefault(OnePlayerData[7], player)
                except IndexError:
                    players = {}
            teams[adatok[0]] = Team(adatok[0], adatok[1], tact, players)
        
        f.close()
        currentSS=slot
        return "Sikeres Betöltés"
    except FileNotFoundError:
        f = open(f"save{slot}.save", "w", encoding="utf-8")
        f.write(" ")
        f.close()
        currentSS=slot
        return "Új fájl létrehozva"
    except ValueError:
        return "Load Failed"

def SimulateMatch(team1: Team, team2: Team, Chances: int=10, MatchLength: int=90):
    for chance in Chances:
        pass

def SetTeamStats(team: Team, debug=False):
    try:
        team.KeeperOverall = team.Players["GK"].Stats["GoalKeeping"]/len(team.Players["GK"].Stats.values()) * team.getTeamWork() / 50
    except KeyError:
        #Team Doesn't have a keeper (probably need a messagebox)
        pass
    for key, player in team.Players.items():
        if "B" in key:
            team.DefOverall += player.Overall*team.TeamWorkOverall/50/4
        elif "M" in key:
            team.MidOverall += player.Overall*team.TeamWorkOverall/50/3
        elif "W" in key or "T" in key:
            team.AttOverall += player.Overall*team.TeamWorkOverall/50/3
        
    if debug:
        print(f"Teamname: {team.Name} Attack Overall: {team.AttOverall} Midfield Overall: {team.MidOverall} Defense Overall: {team.DefOverall} Keeper Overall: {team.KeeperOverall} Teamwork Overall: {team.getTeamWork()}")
# def GetTeamByName(name):
#         for team in Teams.values():
#             if team.Name == name:
#                 return team
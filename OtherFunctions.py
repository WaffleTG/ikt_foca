from Classes import Team, Player
from Data import Teams, currentSS, LastTeam, LastTeam, SaveFileRoute

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
            print(a)
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
                print(data)
                OnePlayerData = data.split(":")
                try:
                    player = Player(OnePlayerData[0], int(OnePlayerData[1]), int(OnePlayerData[2]), int(OnePlayerData[3]), int(OnePlayerData[4]), int(OnePlayerData[5]), int(OnePlayerData[6]), OnePlayerData[7])
                    players.setdefault(OnePlayerData[8], player)
                
                except IndexError:
                    print("Error")
                    players = {}
            teams[adatok[0]] = Team(adatok[0], adatok[1], tact, players)
        
        f.close()
        currentSS=slot
        return "Sikeres Betöltés"
    except FileNotFoundError:
        f = open(f"{SaveFileRoute}save{slot}.save{slot}.save", "w", encoding="utf-8")
        f.write(" ")
        f.close()
        currentSS=slot
        return "Új fájl létrehozva"
    except ValueError:
        return "Load Failed"

def SimulateMatch(team1: Team, team2: Team, Chances: int=10, MatchLength: int=90):
    for chance in Chances:
        pass


        
    
#         for team in Teams.values():
#             if team.Name == name:
#                 return team
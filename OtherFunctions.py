from Classes import Team
from Data import Teams

def Save(slot:int):
    f = open(f"save{slot}.save", "w", encoding="utf-8")
    for team in Teams:
        f.write(f"{team.Name};{team.Formation};")
        for a in team.Tactics:
            f.write(f"{a},")
        f.write(f";")
        for a in team.Players:
            f.write(f"{a},")
    f.close()


def Load(slot:int):
    teams = Teams
    try:
        f = open(f"save{slot}.save", "r", encoding="utf-8")
        for sor in f:
            adatok = sor.strip().split(";")
            tact = adatok[2].split(",")
            players = adatok[3].split(",")
            teams.append(Team(adatok[0], adatok[1], tact, players))
        f.close()
    except:
        f = open(f"save{slot}.save", "w", encoding="utf-8")
        f.write(" ")
        f.close()
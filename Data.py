from Classes import Team
Formations = ("4-4-2", "4-3-3", "3-5-2", "4-2-3-1")
Teams = {"Joe team":Team("Joe team", "4-4-2", [],[])}
PosCords = {
    "GK": (350, 520),
    "CB1": (475, 450),
    "CB2": (225, 450),
    "CB3": (350,450),
    "LB": (75, 430),
    "RB": (625, 430),
    "CM1": (465, 330),
    "CM2": (235, 330),
    "LM": (75, 330),
    "RM": (625, 330),
    "CAM": (350, 250),
    "WAM1": (150, 250),
    "WAM2": (550, 250),
    "LW": (85, 170),
    "RW": (615, 170),
    "ST": (350, 150),
    "RST": (450, 150),
    "LST":(250, 150),
    "SUB1":(5,50),
    "RES1":()
}
LastTeam = None
LastSave = None
currentSS = 1
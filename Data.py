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
    "LST":(250, 150)
}
for i in range(1, 9):
    PosCords.setdefault(f"SUB{i}", (235, 20+i*35))
    PosCords.setdefault(f"RES{i}", (20, 20+i*35))
for i in range(9, 11):
    PosCords.setdefault(f"RES{i}", (20, 20+i*35))
LastTeam = None
LastSave = None
currentSS = 1
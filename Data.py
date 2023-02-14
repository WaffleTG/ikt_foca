Formations = ("4-4-2", "4-3-3", "3-5-2", "4-2-3-1")
Teams = {}
PosCords = {
    "GK": (330, 520),
    "CB1": (445, 450),
    "CB2": (195, 450),
    "CB3": (320,450),
    "LB": (45, 430),
    "RB": (595, 430),
    "CM1": (435, 330),
    "CM2": (205, 330),
    "LM": (45, 330),
    "RM": (595, 330),
    "CAM": (320, 250),
    "WAM1": (120, 250),
    "WAM2": (520, 250),
    "LW": (55, 170),
    "RW": (585, 170),
    "ST": (320, 150),
    "RST": (420, 150),
    "LST":(220, 150)
}
for i in range(1, 9):
    PosCords.setdefault(f"SUB{i}", (235, 20+i*35))
    PosCords.setdefault(f"RES{i}", (20, 20+i*35))
for i in range(9, 11):
    PosCords.setdefault(f"RES{i}", (20, 20+i*35))
LastTeam = 0
currentSS = 1
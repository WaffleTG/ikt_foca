
def addBtnClick(self, mode):
self.clearWindow()
self.TacticsVars = {
    "Defwidth": ctk.IntVar(),
    "Defline": ctk.IntVar(),
    "Agressivness": ctk.IntVar(),
    "Defstyle": ctk.IntVar(),
    "Attackwidth": ctk.IntVar(),
    "Passlength": ctk.IntVar(),
    "Attackspeed": ctk.IntVar(),
    "Shootrate": ctk.IntVar()
}
self.TeamNameVar = ctk.StringVar(value=f"New Team({self.GetNewTeamNum()})")
self.FormationVar = ctk.StringVar()
if mode == "add":
    tacs = {}
    for key in self.TacticsVars.keys():
        tacs.setdefault(key, 50)
    self.ActiveTeam = Team("", "", tacs, {})
if mode == "edit":
    for key, val in self.ActiveTeam.Tactics.items():
        print(key, val)
        self.TacticsVars[key].set(val)
    self.TeamNameVar.set(self.ActiveTeam.Name)
    print("EditMode")


self.columnconfigure(0, weight=1)
self.columnconfigure(1, weight=1)
self.columnconfigure(2, weight=1)
self.columnconfigure(3, weight=1)
self.columnconfigure(4, weight=1)
self.columnconfigure((5,6,7,8,9,10), weight=0)
self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=0)
xPadding = 20
self.HeaderLabel = ctk.CTkLabel(self, font=self.HeaderFont, text="Csapat Hozzáadása").grid(row=0, column=0, columnspan=5, pady=(10,30))

self.NameLabel = ctk.CTkLabel(self, text="Csapat Név", font=self.EntryFont).grid(row=1, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
self.NameEntry = ctk.CTkEntry(self, font=self.EntryFont, width=280, height=40, textvariable=self.TeamNameVar).grid(row=2, column=0 ,padx=(xPadding,0), sticky="w")

self.FormationLabel = ctk.CTkLabel(self, text="Felállás", font=self.EntryFont).grid(row=3, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
self.FormationOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont,dropdown_font=self.EntryFont, values=Formations, variable=self.FormationVar)
self.FormationOption.grid(row=4, column=0, padx=(xPadding,0), sticky="w")
if hasattr(self, "Tactics"):
    self.FormationOption.set(self.ActiveTeam.Formation)
    print(self.ActiveTeam.Formation)
else:
    self.FormationOption.set("4-4-2")
self.AddPlayerButton = ctk.CTkButton(self,text="Csapat Szerkesztése",width=280, height=40, font=self.EntryFont, command=lambda:[self.TeamFormationScreenBtn("add")]).grid(row=5, column=0,rowspan=2, padx=(xPadding,0), sticky="w", pady=(20,0))

self.TacticsLabel = ctk.CTkLabel(self, text="Taktika", font=self.HeaderFont).grid(row=1, column=1, columnspan=4)

self.DefendseLabel = ctk.CTkLabel(self, text="Védekezés", font=self.NormalFont).grid(row=2, column=1,columnspan=2)
self.AttackLabel = ctk.CTkLabel(self, text="Támadás", font=self.NormalFont).grid(row=2, column=3, columnspan=2)

self.DefWidthLabel = ctk.CTkLabel(self, text="Szélesség", font=self.EntryFont).grid(row=3, column=1, columnspan=2)
self.AttackWidthLabel = ctk.CTkLabel(self, text="Szélesség", font=self.EntryFont).grid(row=3, column=3, columnspan=2)
self.SpaceLabel1 = ctk.CTkLabel(self, text="    ", font=self.NormalFont).grid(row=3, column=1, padx=(0,30))
self.SpaceLabel2 = ctk.CTkLabel(self, text="    ", font=self.NormalFont).grid(row=3, column=3, padx=(30,0))
self.DefWidthVarLabel = ctk.CTkLabel(self, textvariable=self.TacticsVars["Defwidth"], font=self.EntryFont).grid(row=4, column=1, sticky="e",padx=10)
self.DefWidthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.TacticsVars["Defwidth"]).grid(row=4, column=2, sticky="w", padx=(0,40))
self.AttackWidthVarLabel = ctk.CTkLabel(self, textvariable=self.TacticsVars["Attackwidth"], font=self.EntryFont).grid(row=4, column=3, sticky="e",padx=10)
self.AttackWidthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.TacticsVars["Attackwidth"]).grid(row=4, column=4, sticky="w", padx=(0,40))

self.DefLineLabel = ctk.CTkLabel(self, text="Védővonal", font=self.EntryFont).grid(row=5, column=1, columnspan=2)
self.PassLengthLabel = ctk.CTkLabel(self, text="Passzok Hossza", font=self.EntryFont).grid(row=5, column=3, columnspan=2)

self.DefLineVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Defline"], font=self.EntryFont).grid(row=6, column=1, sticky="e",padx=10)
self.DefLineSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.TacticsVars["Defline"]).grid(row=6, column=2, sticky="w", padx=(0,40))
self.PassLengthVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Passlength"], font=self.EntryFont).grid(row=6, column=3, sticky="e",padx=10)
self.PassLengthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.TacticsVars["Passlength"]).grid(row=6, column=4, sticky="w", padx=(0,40))

self.AgressivnessLabel = ctk.CTkLabel(self, text="Agresszivitás", font=self.EntryFont).grid(row=7, column=1, columnspan=2)
self.AttackSpeedLabel = ctk.CTkLabel(self, text="Gyorsaság", font=self.EntryFont).grid(row=7, column=3, columnspan=2)

self.AgressivnessVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Agressivness"], font=self.EntryFont).grid(row=8, column=1, sticky="e",padx=10)
self.AgressivnessSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.TacticsVars["Agressivness"]).grid(row=8, column=2, sticky="w", padx=(0,40))
self.AttackSpeedVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Attackspeed"], font=self.EntryFont).grid(row=8, column=3, sticky="e",padx=10)
self.AttackSpeedSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.TacticsVars["Attackspeed"]).grid(row=8, column=4, sticky="w", padx=(0,40))

self.DefStyleLabel = ctk.CTkLabel(self, text="Emberfogás", font=self.EntryFont).grid(row=9, column=1, columnspan=2)
self.ShootRateLabel = ctk.CTkLabel(self, text="Lövésgyakoriság", font=self.EntryFont).grid(row=9, column=3, columnspan=2)

self.DefStyleVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Defstyle"], font=self.EntryFont).grid(row=10, column=1, sticky="e",padx=10)
self.DefStyleSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.TacticsVars["Defstyle"]).grid(row=10, column=2, sticky="w", padx=(0,40))
self.ShootRateVarLabel = ctk.CTkLabel(self, textvariable = self.TacticsVars["Shootrate"], font=self.EntryFont).grid(row=10, column=3, sticky="e",padx=10)
self.ShootRateSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.TacticsVars["Shootrate"]).grid(row=10, column=4, sticky="w", padx=(0,40))

self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.EditBtnClick).grid(row=11, column=0, sticky="w", pady=(120,0), padx=xPadding)
self.SaveTeam = ctk.CTkButton(self, 120, 40, text="Taktika Mentése", font=self.ButtonFont, command=self.SaveActiveTeam).grid(row=11, column=4, sticky="w", pady=(120,0), padx=xPadding)

def TeamFormationScreenBtn(self, mode):
self.clearWindow()
self.NameVariables = {}
if mode == "edit":
    pass
for key, val in self.TacticsVars.items():
    self.ActiveTeam.Tactics[key] = val.get()
for pos in PosCords.keys():
    self.NameVariables.setdefault(pos, ctk.StringVar(value=pos))
try:
    for key, val in self.ActiveTeam.Players.items():
        self.NameVariables[key] = ctk.StringVar(value=val.Name)
except AttributeError:
    pass
if mode == "add":
    if self.ActiveTeam.Name.strip() != "":
        self.ActiveTeam.Name = self.TeamNameVar.get()
        
    else:
        self.ActiveTeam.Name = f"New Team({self.GetNewTeamNum()})"
        print(self.ActiveTeam.Name)
    Teams.setdefault(self.ActiveTeam.Name, self.ActiveTeam)
    # #addteam
    # self.ActiveTeam = Team(self.TeamNameVar.get(), self.FormationVar.get(), tactics=self.Tactics, players={})
    # Teams[self.ActiveTeam.Name]= self.ActiveTeam
# if mode == "edit":

self.ActiveTeam.Name = self.TeamNameVar.get()
self.ActiveTeam.Formation = self.FormationVar.get()

self.columnconfigure(0, weight=1)
self.columnconfigure(1, weight=1)
self.columnconfigure(2, weight=4)
self.rowconfigure(0, weight=0)
self.rowconfigure(1, weight=0)
self.rowconfigure(2, weight=0)
self.rowconfigure(3, weight=0)
self.rowconfigure(4, weight=0)
StarterLabelBgColor = "dark green"
SubLabelBgColor = "green4"
self.LabelCursor = "circle"

self.FormationFrame = ctk.CTkFrame(self, width=700,height=580, fg_color="green")
self.FormationFrame.grid(row=0, column=2,rowspan=5, sticky="e")
self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=lambda: self.addBtnClick("edit")).grid(row=3, column=0, sticky="nw", padx=20, pady=(80,0))
self.GKLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["GK"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor)
self.GKLabel.place(x=PosCords["GK"][0], y=PosCords["GK"][1])
self.CB1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CB1"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB1"][0],y=PosCords["CB1"][1])
self.CB2Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CB2"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB2"][0],y=PosCords["CB2"][1])
self.CM1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM1"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CM1"][0], y=PosCords["CM2"][1])
self.CM2Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM2"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CM2"][0], y=PosCords["CM2"][1])
if self.FormationVar.get() == "3-5-2":  
    self.CB3Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM2"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB3"][0],y=PosCords["CB3"][1])
else:
    self.LBLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LB"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LB"][0], y=PosCords["LB"][1])
    self.RBLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RB"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RB"][0], y=PosCords["RB"][1])

if self.FormationVar.get() != "4-4-2":
    self.CAMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CAM"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CAM"][0], y=PosCords["CAM"][1])
 
if self.FormationVar.get() == "4-3-3":
    self.LWLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LW"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LW"][0], y=PosCords["LW"][1])
    self.RWLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RW"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RW"][0], y=PosCords["RW"][1])
    self.STLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["ST"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["ST"][0], y=PosCords["ST"][1])
elif self.FormationVar.get() == "4-2-3-1":
    self.WAM2abel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["WAM2"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["WAM1"][0], y=PosCords["WAM1"][1])
    self.WAM1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["WAM1"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["WAM2"][0], y=PosCords["WAM2"][1])
    self.STLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["ST"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["ST"][0], y=PosCords["ST"][1])
else:
    self.LMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LM"],font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LM"][0], y=PosCords["LM"][1])
    self.RMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RM"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RM"][0], y=PosCords["RM"][1])
    self.LSTLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LST"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LST"][0], y=PosCords["LST"][1])
    self.RSTLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RST"], font=self.FormationFont, fg_color=StarterLabelBgColor, bg_color=StarterLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RST"][0], y=PosCords["RST"][1])

self.ReserveFrame = ctk.CTkFrame(self, width=400)
self.ReserveFrame.grid(row=0,column=0,rowspan=3,columnspan=2, sticky="n")  


self.SubAlign = ctk.CTkLabel(self.ReserveFrame,text="                                                    ", font=self.HeaderFont).pack(pady=(0,400))
self.ReserveLabel = ctk.CTkLabel(self.ReserveFrame,text="Tartalékok", font=self.HeaderFont).place(x=20, y=10)
self.SubLabel = ctk.CTkLabel(self.ReserveFrame,text="Cserék", font=self.HeaderFont).place(x=235, y=10)

self.Res1Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES1"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor)
self.Res1Label.place(x=PosCords["RES1"][0],y=PosCords["RES1"][1])
self.Res2Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES2"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES2"][0],y=PosCords["RES2"][1])
self.Res3Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES3"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES3"][0],y=PosCords["RES3"][1])
self.Res4Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES4"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES4"][0],y=PosCords["RES4"][1])
self.Res5Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES5"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES5"][0],y=PosCords["RES5"][1])
self.Res6Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES6"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES6"][0],y=PosCords["RES6"][1])
self.Res7Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES7"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES7"][0],y=PosCords["RES7"][1])
self.Res8Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES8"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES8"][0],y=PosCords["RES8"][1])
self.Res9Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES9"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES9"][0],y=PosCords["RES9"][1])
self.Res10Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["RES10"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RES10"][0],y=PosCords["RES10"][1])

self.Sub1Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB1"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB1"][0],y=PosCords["SUB1"][1])
self.Sub2Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB2"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB2"][0],y=PosCords["SUB2"][1])
self.Sub3Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB3"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB3"][0],y=PosCords["SUB3"][1])
self.Sub4Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB4"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB4"][0],y=PosCords["SUB4"][1])
self.Sub5Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB5"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB5"][0],y=PosCords["SUB5"][1])
self.Sub6Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB6"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB6"][0],y=PosCords["SUB6"][1])
self.Sub7Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB7"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB7"][0],y=PosCords["SUB7"][1])
self.Sub8Label = ctk.CTkLabel(self.ReserveFrame, textvariable = self.NameVariables["SUB8"], font=self.FormationFont, fg_color=SubLabelBgColor, bg_color=SubLabelBgColor, cursor=self.LabelCursor).place(x=PosCords["SUB8"][0],y=PosCords["SUB8"][1])

self.FormationFrame.bind_class('Label', "<Button-1>", self.FormationLabelClick)
self.FormationFrame.bind_class('Label', "<Button-3>", self.PlayerEditClick)

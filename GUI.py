import random
import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk
from Data import Teams, Formations, PosCords, LastTeam, currentSS, GameModes, ChanceCountModes
from OtherFunctions import Save, Load
from Classes import Player, Team, Chance
import webbrowser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.ButtonFont = ('Helvetica', 26, 'bold')
        self.EntryFont = ('Helvetica', 20, 'bold')
        self.HeaderFont = ('Helvetica', 30, 'bold')
        self.NormalFont = ('Helvetica', 24, 'bold')
        self.FormationFont = ('Helvetica', 16, 'bold')

        self.SimNumFont = ('Helvetica', 100, 'bold')
        self.SimTeamFont = ('Helvetica', 36, 'bold')
        self.ActiveTeam = LastTeam
        self.geometry("1100x580")
        self.title("Football Simulation")
        self.resizable(False, False)
        self.StartScreen()            
        self.bind_class('Entry', '<Control-BackSpace>', self.entry_ctrl_bs)
    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.unbind_class('Label', '<Button-1>')
        self.unbind_class('Label','<Button-3>')

    def entry_ctrl_bs(self, event):
        ent = event.widget
        end_idx = ent.index(ctk.INSERT)
        start_idx = ent.get().rfind(" ", None, end_idx)
        ent.delete(start_idx, end_idx) 


    def LoadFinish(self, szoveg):
        self.clearWindow()
        self.AlertLabel = ctk.CTkLabel(self, font=self.HeaderFont, text=szoveg)
        self.AlertLabel.pack(pady=30)

        self.ContinueBtn = ctk.CTkButton(self, 300, 80, text="Folytatás", font=self.ButtonFont, command=self.StartScreen)
        self.ContinueBtn.pack(pady=30)

    def ChooseSaveSlot(self):
        self.clearWindow()
        
        self.slot1Btn = ctk.CTkButton(self, 400,80, text="Első mentés", font=self.ButtonFont, command=lambda:[self.LoadFinish(Load(1))])
        self.slot1Btn.pack(pady=30)

        self.slot2Btn = ctk.CTkButton(self, 400, 80, text="Második mentés", font=self.ButtonFont, command=lambda:[self.LoadFinish(Load(2))])
        self.slot2Btn.pack(pady=0)

        self.slot3Btn = ctk.CTkButton(self, 400, 80, text="Harmadik mentés", font=self.ButtonFont, command=lambda:[self.LoadFinish(Load(3))])
        self.slot3Btn.pack(pady=30)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.StartScreen)
        self.BackBtn.pack(side=tk.BOTTOM, padx=10, anchor="w", pady=10)

    def StartScreen(self):
        self.clearWindow()
        self.PlayBtn = ctk.CTkButton(self, 400, 80, text="Játék Számítógép ellen", font=self.ButtonFont, command=self.GameVsAi)
        self.PlayBtn.pack(pady=30)
        if len(Teams)>0:
            self.PlayBtn.configure(state="normal")

        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapatok szerkesztése", font=self.ButtonFont, command=self.EditBtnClick)
        self.EditBtn.pack(pady=0)
        
        self.SpecialModeBtn = ctk.CTkButton(self, 400, 80, text="Speciális játékmód", font=self.ButtonFont)
        self.SpecialModeBtn.pack(pady=(30,0))

        self.LoadSaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés betöltése", font=self.ButtonFont, command=self.ChooseSaveSlot)
        self.LoadSaveBtn.pack(pady=30)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="About", font=self.ButtonFont, command=self.AboutClick)
        self.BackBtn.pack(side=tk.BOTTOM, padx=10, anchor="w", pady=10)

    def AboutClick(self):
        webbrowser.open("https://google.com/")

    def GameVsAi(self):
        if len(Teams) == 0:
            tkm.showinfo(title="Nem Lehet Játékot Indítani!", message="Nincs egy csapat se elmentve!")
        else:
            self.clearWindow()
            
            self.columnconfigure((0,1,2,3), weight=1)
            self.rowconfigure((0,1,2,3,4,5), weight=0)
            try:
                self.team1Var.set(self.ActiveTeam.Name)
            except AttributeError:
                self.team1Var = ctk.StringVar(value=Teams[list(Teams.keys())[0]].Name)
            
            self.team2Var = ctk.StringVar(value=Teams[list(Teams.keys())[0]].Name)
            

            self.gameModeVar = ctk.StringVar(value=GameModes[0])
            self.ChanceCountVar = ctk.IntVar(value=10)
            self.GameLengthVar = ctk.IntVar(value=90)
            if len(Teams) > 1:
                self.team2Var.set(Teams[list(Teams.keys())[1]].Name)
                
            Teams[self.team1Var.get()].SetStats(True)
            Teams[self.team2Var.get()].SetStats(True)
            #1.Sor
            self.HeadLabel = ctk.CTkLabel(self,text="Válassz Csapatokat",font=self.HeaderFont).grid(column=0, columnspan=4, row=0, pady=(20,10))

            #2.Sor
            self.Team1Option = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.team1Var)
            self.Team1Option.grid(column=1, row=1, pady=20)
            self.Team2Option = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.team2Var).grid(column=2, row=1, pady=20)
            self.Rand1Button = ctk.CTkButton(self, 40, 40, text="🎲", font=self.ButtonFont, command=lambda: self.RandomiseTeam(0)).grid(column=0, row=1, sticky="e")
            self.Rand2Button = ctk.CTkButton(self, 40, 40, text="🎲", font=self.ButtonFont, command=lambda: self.RandomiseTeam(1)).grid(column=3, row=1, sticky="w")

            #3.Sor
            self.Att1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Támadás: {Teams[self.team1Var.get()].AttOverall:.0f}")
            self.Att1Label.grid(column=1, row=2, sticky="w", padx=(55,0))
            self.Att2Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Támadás: {Teams[self.team2Var.get()].AttOverall:.0f}")
            self.Att2Label.grid(column=2, row=2, sticky="w", padx=(55,0))
            #4.Sor
            self.Mid1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Középpálya: {Teams[self.team1Var.get()].MidOverall:.0f}")
            self.Mid1Label.grid(column=1, row=3, sticky="w", padx=(55,0))
            self.Mid2Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Középpálya: {Teams[self.team2Var.get()].MidOverall:.0f}")
            self.Mid2Label.grid(column=2, row=3, sticky="w", padx=(55,0))
            #5.Sor
            self.Def1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Védelem: {Teams[self.team1Var.get()].DefOverall:.0f}")
            self.Def1Label.grid(column=1, row=4, sticky="w", padx=(55,0))
            self.Def2Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Védelem: {Teams[self.team2Var.get()].DefOverall:.0f}")
            self.Def2Label.grid(column=2, row=4 , sticky="w", padx=(55,0))
            #6.Sor
            self.TeamWork1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Összhang: {Teams[self.team1Var.get()].getTeamWork():.0f}")
            self.TeamWork1Label.grid(column=1, row=5, sticky="w", padx=(55,0))
            self.TeamWork2Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Összhang: {Teams[self.team2Var.get()].getTeamWork():.0f}")
            self.TeamWork2Label.grid(column=2, row=5 , sticky="w", padx=(55,0))

            self.team1Var.trace("w", lambda *args: self.UpdateLabels(args, 0))
            self.team2Var.trace("w", lambda *args: self.UpdateLabels(args, 1))
            

            #7-8.Sor
            self.GameModeChoiceLabel = ctk.CTkLabel(self, font=self.EntryFont, text="Játékmód").grid(column=1, row=6, pady=(20,0), sticky="w", padx=(60,0))
            self.ChanceCountChoiceLabel = ctk.CTkLabel(self, font=self.EntryFont, text="Helyzetek Száma").grid(column=2, row=6, pady=(20,0), sticky="w", padx=(60,0))
            self.GameModeChoice = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=GameModes).grid(column=1, row=7, pady=(0,30))
            self.ChanceCountChoice = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(ChanceCountModes.keys()), command=self.UpdateChanceCount).grid(column=2, row=7, pady=(0,30))
            #9-10.Sor
            self.GameLengthLabel = ctk.CTkLabel(self, font=self.EntryFont, text=f"Meccs Hossza: {self.GameLengthVar.get()} Perc")
            self.GameLengthLabel.grid(row=8,column=1, padx=(0,40))
            self.GameLengthSlider = ctk.CTkSlider(self, width=280, height=26,from_=30, to=180, number_of_steps=150,variable=self.GameLengthVar, command=self.UpdateLengthSlider).grid(row=9, column=1)
            #11.sor
            
            self.GameStartButton = ctk.CTkButton(self, 280, 40, text="Játék indítása", font=self.EntryFont, command=lambda:self.SimulationScreen(Teams[self.team1Var.get()], Teams[self.team2Var.get()],self.ChanceCountVar.get(), self.GameLengthVar.get() )).grid(column=2, row=10)
    def UpdateChanceCount(self, *args):
        self.ChanceCountVar.set(ChanceCountModes[args[0]])
    def UpdateLengthSlider(self, *args):
        self.GameLengthLabel.configure(text=f"Meccs Hossza: {args[0]:.0f} Perc")
    def UpdateLabels(self, *args):
        if args[1] == 0:
            self.Att1Label.configure(text=f"Támadás: {Teams[self.team1Var.get()].AttOverall:.0f}")
            self.Mid1Label.configure(text=f"Középpálya: {Teams[self.team1Var.get()].MidOverall:.0f}")
            self.Def1Label.configure(text=f"Védelem: {Teams[self.team1Var.get()].DefOverall:.0f}")
            self.TeamWork1Label.configure(text=f"Összhang: {Teams[self.team1Var.get()].getTeamWork():.0f}")
        else:
            self.Att2Label.configure(text=f"Támadás: {Teams[self.team2Var.get()].AttOverall:.0f}")
            self.Mid2Label.configure(text=f"Középpálya: {Teams[self.team2Var.get()].MidOverall:.0f}")
            self.Def2Label.configure(text=f"Védelem: {Teams[self.team2Var.get()].DefOverall:.0f}")
            self.TeamWork2Label.configure(text=f"Összhang: {Teams[self.team2Var.get()].getTeamWork():.0f}")
    def RandomiseTeam(self, teamNum = 0):
        if teamNum == 0:
            self.team1Var.set(Teams[list(Teams.keys())[random.randint(0,len(Teams)-1)]].Name)
        elif teamNum == 1:
            self.team2Var.set(Teams[list(Teams.keys())[random.randint(0,len(Teams)-1)]].Name)
    def SimulationScreen(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90):
        team1.SetStats(True)
        team2.SetStats(True)
        self.clearWindow()
        self.speedVar = ctk.IntVar(value=1)
        self.timeVar = ctk.IntVar(value=0)
        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1,3,4,5,6), weight=0)
        self.rowconfigure(2, weight=0)
        self.ScoreList = [0, 0]
        self.Score = ctk.StringVar(value=f"{self.ScoreList[0]}  -  {self.ScoreList[1]}")
        #első sor
        self.TimeLabel = ctk.CTkLabel(self, textvariable = self.timeVar, font=self.SimNumFont).grid(column=1,columnspan=3,row=0)
        self.StatButton = ctk.CTkButton(self, 40,40, text="Statisztika", font=self.EntryFont).grid(column=4, row=0)
        
        #második sor
        self.Team1Label = ctk.CTkLabel(self, text=team1.Name, font=self.SimTeamFont).grid(column=0 ,row=1, sticky="e")
        self.ScoreLabel = ctk.CTkLabel(self, textvariable = self.Score, font=self.SimNumFont).grid(column=1,columnspan=3,row=1)
        self.Team2Label = ctk.CTkLabel(self, text=team2.Name, font=self.SimTeamFont).grid(column=4 ,row=1, sticky="w")
        
        #harmadik sor
        self.CommentaryBox = ctk.CTkFrame(self, width=900, height=150).grid(column=0,columnspan=5 ,row=2)
        
        #negyedik sor
        self.StartButton = ctk.CTkButton(self, 200,40, text="Szimuláció indítása", font=self.EntryFont, command=lambda: self.StartSim(team1, chances, ChanceCount, MatchLength, self.timeVar.get()))
        self.StartButton.grid(column=0, row=3, pady=20, padx=(60,0))
        self.StopButton = ctk.CTkButton(self, 200,40, text="Szimuláció Megállítása", font=self.EntryFont, command=self.StopSim, state="disabled")
        self.StopButton.grid(column=1, row=3, pady=20)
        
        chances = self.GenerateSimulation(team1, team2, ChanceCount, MatchLength)[0] 
        #Simulation
    def tksleep(self, time:float) -> None:
        self.after(int(time*1000), self.quit)
        self.mainloop()
    def StartSim(self, team1, chances, ChanceCount, MatchLength, Begin):
        self.run =  True
        self.StartButton.configure(state="disabled")
        self.StopButton.configure(state="normal")
        
        for i in range(Begin,MatchLength+random.randint(2, int(MatchLength/ChanceCount))):
            if self.run:
                self.timeVar.set(i)
                if i in chances.keys():
                    
                    if chances[i].IsGoal:
                        if chances[i].Team.Name == team1.Name:
                            self.ScoreList[0] += 1
                        else:
                            self.ScoreList[-1] += 1
                self.Score.set(f"{self.ScoreList[0]}  -  {self.ScoreList[1]}")
                self.tksleep(0.33/self.speedVar.get())
            else:
                return

    def StopSim(self):
        self.run = False
        self.StopButton.configure(state="disabled")
        self.StartButton.configure(state="normal")

    def GenerateSimulation(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90):
        team1.SetStats(True)
        team2.SetStats(True)
        Chances = {}
        for i in range(1, int(ChanceCount)+2):
            AttTeam = random.randint(0, int(team1.MidOverall + team2.MidOverall))
            # print(AttTeam, team1.MidOverall /100 * 95, team1.MidOverall/100*95)
            if AttTeam < team1.MidOverall /100 * 95:
                AttTeam = team1
                DefTeam = team2
            elif AttTeam < (team1.MidOverall + team2.MidOverall) / 100 * 95:
                AttTeam = team2
                DefTeam = team1
            else:
                continue
            ChanceTime = random.randint((i-1) * int(MatchLength/ChanceCount) + 1 ,((i) * int(MatchLength/ChanceCount)))

            GoalChance = random.randint(0, int(AttTeam.AttOverall /100 * 95) + int(DefTeam.DefOverall))
            if GoalChance < DefTeam.DefOverall:
                IsGoal = True
            else:
                IsGoal = False
            Chances.setdefault(ChanceTime, Chance(ChanceTime, AttTeam, IsGoal))
        golok = [0,0]
        for x in Chances.values():
            if x.IsGoal:
                if x.Team.Name == team1.Name:
                    golok[0] += 1
                else:
                    golok[1] += 1
        return Chances, golok
        
    def SimTest(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90, simAmount=1000):
        ossz1Golok = 0 
        ossz2Golok = 0
        for i in range(0, simAmount):
            golok = self.GenerateSimulation(team1, team2, ChanceCount, MatchLength)[1]
            
            ossz1Golok += golok[0]
            ossz2Golok += golok[1]

        print(f"{ossz1Golok/simAmount} - {ossz2Golok/simAmount}")
    def EditBtnClick(self):
        self.clearWindow()
        print(self.ActiveTeam)
        self.addBtn = ctk.CTkButton(self, 400, 80, text="Csapat Hozzáadása", font=self.ButtonFont, command=lambda: self.addBtnClick("add"))
        self.addBtn.pack(pady=30)

        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapat Szerkesztése", font=self.ButtonFont, command=lambda: self.ChooseTeam("edit"))
        self.EditBtn.pack(pady=0)

        self.DeleteBtn = ctk.CTkButton(self, 400, 80, text="Csapat Törlése", font=self.ButtonFont, command=lambda: self.ChooseTeam("delete"))
        self.DeleteBtn.pack(pady=30)

        self.SaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés", font=self.ButtonFont, command= lambda: Save(currentSS))
        self.SaveBtn.pack(pady=0)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.StartScreen)
        self.BackBtn.pack(side=tk.BOTTOM, padx=10, anchor="w", pady=10)

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
        self.AddPlayerButton = ctk.CTkButton(self,text="Csapat Szerkesztése",width=280, height=40, font=self.EntryFont, command=lambda:[self.TeamFormationScreenBtn(mode)]).grid(row=5, column=0,rowspan=2, padx=(xPadding,0), sticky="w", pady=(20,0))

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
            print(self.ActiveTeam.Players)
            for key, val in self.ActiveTeam.Players.items():
                self.NameVariables[key] = ctk.StringVar(value=val.Name)
        except AttributeError:
            pass
        if mode == "add":
            if self.TeamNameVar.get().strip() != "":
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
        
             
    def FormationLabelClick(self, event):
        #majd try: except attributeError: pass
        try:
            if event.widget.cget('cursor') == self.LabelCursor:
                print("FormationLabelClick")
                thisPos = self.GetPlayerPos(event.widget)
                if self.NameVariables[thisPos].get() == thisPos:
                    #Insta Create Player

                    self.CreatePlayerBtn(thisPos)
                else:
                    #Bind Click on another player to switch

                    self.FormationFrame.bind_class('Label', '<Button-1>', lambda event, a=event.widget:self.PlayerSwitchByName(event=event, widget1=a), add=False)
        except AttributeError:
            pass

    def PlayerEditClick(self, event):
        try:
            if event.widget.cget('cursor') == self.LabelCursor:
                self.CreatePlayerBtn(self.GetPlayerPos(event.widget))
        except AttributeError:
            pass

    def PlayerSwitchByName(self, widget1, event):
        try:
            if event.widget.cget('cursor') == self.LabelCursor:
                print("PlayerSwitchByName")
                widget2 = event.widget
                if widget2 == widget1:
                    return
                self.FormationFrame.bind_class('Label', '<Button-1>', self.FormationLabelClick, add=False)
                W1Pos = self.GetPlayerPos(widget1)
                W2Pos = self.GetPlayerPos(widget2)
                if W2Pos in self.ActiveTeam.Players.keys():
                    TmpPlayer2 = self.ActiveTeam.Players[W2Pos]
                    self.ActiveTeam.Players[W2Pos] = self.ActiveTeam.Players[W1Pos] 
                    self.ActiveTeam.Players[W1Pos] = TmpPlayer2
                    self.NameVariables[W1Pos].set(self.ActiveTeam.Players[W1Pos].Name)
                    self.NameVariables[W2Pos].set(self.ActiveTeam.Players[W2Pos].Name)
                else:
                    self.ActiveTeam.Players.setdefault(W2Pos, self.ActiveTeam.Players[W1Pos])
                    self.ActiveTeam.Players.pop(W1Pos)
                    self.NameVariables[W2Pos].set(self.ActiveTeam.Players[W2Pos].Name) 
                    self.NameVariables[W1Pos].set(W1Pos)
        except AttributeError:
            pass
        
    def GetPlayerPos(self, widget):
        
        frame = self.nametowidget(self.nametowidget(widget.winfo_parent()).winfo_parent())
        
        if id(frame) == id(self.FormationFrame) :
            xOffest = self.GKLabel.winfo_rootx() - PosCords["GK"][0]
            yOffset = self.GKLabel.winfo_rooty() - PosCords["GK"][1] + 4
        elif id(frame) == id(self.ReserveFrame):
            xOffest = self.Res1Label.winfo_rootx() - PosCords["RES1"][0]
            yOffset = self.Res1Label.winfo_rooty() - PosCords["RES1"][1]+4
        LabelPos = (widget.winfo_rootx() - xOffest, widget.winfo_rooty() - yOffset)
        return list(PosCords.keys())[list(PosCords.values()).index(LabelPos)]

    def CreatePlayerBtn(self, pos):
        self.clearWindow()
        PlayerPositions = []
        for posititon in self.NameVariables.keys():
            PlayerPositions.append(''.join(filter(lambda x: not x.isdigit(), posititon)))
        PlayerPositions = list(set(PlayerPositions))
        PlayerPositions.remove("SUB")
        PlayerPositions.remove("RES")
        
        #Formatting List To Correct Order
        tmpList = [i [::-1] for i in PlayerPositions]
        tmpList.sort()
        PlayerPositions = [i [::-1] for i in tmpList]
        PlayerPositions.remove("GK")
        PlayerPositions.insert(0, "GK")
        PlayerPositions.remove("CAM")
        PlayerPositions.remove("WAM")
        PlayerPositions.insert(7, "CAM")
        PlayerPositions.insert(8, "WAM")
        
        self.PlayerNameVar = ctk.StringVar(value="Enter Player Name")
        try:
            self.PlayerPosVar = ctk.StringVar(value=self.ActiveTeam.Players[pos].Position)
        except KeyError:
            if pos in PlayerPositions:
                self.PlayerPosVar = ctk.StringVar(value=pos)
            else:
                self.PlayerPosVar = ctk.StringVar(value=PlayerPositions[0])
        if self.NameVariables[pos].get() != pos:
            #Edit Player
            self.PlayerNameVar.set(self.NameVariables[pos].get())
            self.CreatedPlayer = self.ActiveTeam.Players[pos]
            self.PlayerPosVar.set(self.CreatedPlayer.Position)
            addBtnText = "Szerkesztés Befejezése"
        else:
            self.CreatedPlayer = Player(self.PlayerNameVar.get(), 50,50,50,50,50,50,pos)
            addBtnText = "Hozzáadás"

        self.StatVars = {}
        for key in self.CreatedPlayer.Stats.keys():
            self.StatVars.setdefault(key, ctk.IntVar(value=self.CreatedPlayer.Stats[key]))

        self.columnconfigure((0,1,2,3), weight=1)
        self.columnconfigure(4, weight=0)
        self.rowconfigure((0,1,2,3,4), weight=0)
        self.rowconfigure(5, weight=1)
  
        self.HeaderLabel = ctk.CTkLabel(self,text="Játékos Hozzáadása", font=self.HeaderFont).grid(row=0, column=0,columnspan=4, pady=(20,40))

        #column0
        self.PlayerNamLabel = ctk.CTkLabel(self,text="Player Name", font=self.NormalFont).grid(row=1, column=0, sticky="w", padx=(20,0))
        self.PlayerNameEntry = ctk.CTkEntry(self, font=self.EntryFont, width=280, height=40, textvariable=self.PlayerNameVar).grid(row=2, column=0, sticky="w", padx=(20,0), pady=(5,20))
        self.PlayerPosLabel = ctk.CTkLabel(self,text="Játékos Pozíciója", font=self.NormalFont).grid(row=3, column=0, sticky="w", padx=(20,0))
        self.PlayerPosOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont,dropdown_font=self.EntryFont, values=PlayerPositions, variable=self.PlayerPosVar).grid(row=4, column=0, sticky="w", padx=(20,0))
        self.AddButon = ctk.CTkButton(self, width=280,height=40, text=addBtnText, font=self.ButtonFont, command= lambda: self.CreatePlayer(pos)).grid(row=5, column=0, sticky="w", padx=(20,0))
        #column1-3
    
        self.StatSetFrame = ctk.CTkFrame(self, width=900, height=350)
        self.StatSetFrame.grid(row=1, column=1, columnspan=4, rowspan=6, sticky="n")
        
        self.StatSetFrame.columnconfigure((0,2,3), weight=0)
        self.StatSetFrame.columnconfigure((1,4), weight=1)
        self.StatSetFrame.rowconfigure((0,1,2,3,4,5,6), weight=0)

        self.PaceVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Pace"], font=self.NormalFont).grid(row=1, column=0)
        self.PaceSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99,variable=self.StatVars["Pace"]).grid(row=1, column=1, sticky="w")
        self.PassingVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Passing"], font=self.NormalFont).grid(row=1, column=3)
        self.PassingSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99, variable=self.StatVars["Passing"]).grid(row=1, column=4, sticky="w")

        self.Gap = ctk.CTkLabel(self.StatSetFrame, text="", font=self.NormalFont).grid(row=0, column=2, padx=50)
        self.PaceLabel = ctk.CTkLabel(self.StatSetFrame, text="Gyorsaság", font=self.NormalFont).grid(row=0, column=1)
        self.PassingLabel = ctk.CTkLabel(self.StatSetFrame, text="Passzolás", font=self.NormalFont).grid(row=0, column=4)
        self.SpaceLabel1 = ctk.CTkLabel(self.StatSetFrame, text="  ", font=self.NormalFont).grid(row=0, column=0, padx=(0,30))
        self.SpaceLabel2 = ctk.CTkLabel(self.StatSetFrame, text="  ", font=self.NormalFont).grid(row=0, column=3, padx=(30,0))

        self.ShotVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Attacking"], font=self.NormalFont).grid(row=3, column=0)
        self.ShotSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99,variable=self.StatVars["Attacking"]).grid(row=3, column=1, sticky="w")
        self.DefVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Defending"], font=self.NormalFont).grid(row=3, column=3)
        self.DefSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99, variable=self.StatVars["Defending"]).grid(row=3, column=4, sticky="w")

        self.ShotLabel = ctk.CTkLabel(self.StatSetFrame, text="Támadás", font=self.NormalFont).grid(row=2, column=1)
        self.DefLabel = ctk.CTkLabel(self.StatSetFrame, text="Védekezés", font=self.NormalFont).grid(row=2, column=4)

        self.TeamworkVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Teamwork"], font=self.NormalFont).grid(row=5, column=0)
        self.TeamworkSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99,variable=self.StatVars["Teamwork"]).grid(row=5, column=1, sticky="w")
        self.GoalkeeperVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["GoalKeeping"], font=self.NormalFont).grid(row=5, column=3)
        self.GoalkeeperSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=0, to=99, number_of_steps=99, variable=self.StatVars["GoalKeeping"]).grid(row=5, column=4, sticky="w")

        self.TeamworkLabel = ctk.CTkLabel(self.StatSetFrame, text="Csapatmunka", font=self.NormalFont).grid(row=4, column=1)
        self.GoalkeeperLabel = ctk.CTkLabel(self.StatSetFrame, text="Vetődés", font=self.NormalFont).grid(row=4, column=4)

    def ChooseTeam(self, action):
        if len(Teams) == 0:
            tkm.showinfo(title="Nem Lehet Szerkeszteni Csapatot!",message="Nincs egy csapat se elmentve!")
        else:
            self.clearWindow()
            if self.ActiveTeam == None:
                self.ActiveTeam = Teams[list(Teams.keys())[0]]
            try:
                if self.ActiveTeam.Name not in Teams.keys():
                    self.ActiveTeam = Teams[list(Teams.keys())[0]]
            except:
                self.ActiveTeam = Teams[list(Teams.keys())[0]]
            self.SelectedTeamVar = ctk.StringVar(value=self.ActiveTeam.Name)
            self.HeadLabel = ctk.CTkLabel(self, text="Válaszd ki a csapatot amit ki szeretnél törölni", font=self.HeaderFont)
            self.HeadLabel.pack(pady=10)
            print(Teams.keys())
            self.TeamChoiceOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.SelectedTeamVar)
            self.TeamChoiceOption.pack(pady=10)
            print(self.ActiveTeam.Name)
            self.SelectedTeamVar.set(self.ActiveTeam.Name)
            
                
            self.ChooseButton = ctk.CTkButton(self, 300, 80, text="Törlés", font=self.ButtonFont, command=lambda:self.DeleteTeam(self.TeamChoiceOption.get()))
            self.ChooseButton.pack(pady=10)
            if action == "edit":
                self.ChooseButton.configure(text="Szerkesztés")
                try:
                    self.ActiveTeam = Teams[self.TeamChoiceOption.get()]
                except KeyError:
                    self.ActiveTeam = Teams[list(Teams.keys())[0]]
                self.ChooseButton.configure(command=lambda: self.EditTeam(self.TeamChoiceOption.get()))
                self.HeadLabel.configure(text="Válaszd ki a csapatot amit szerkeszteni szeretnél")
        # self.ActiveTeam.SetStats(True)
    
    def DeleteTeam(self, name):
        answer = tkm.askyesno(title="Csapat Törlése", message=f"Biztos vagy benne hogy törölni szeretnék a {name} nevű csapatot?")
        if answer:
            self.ActiveTeam = Teams[list(Teams.keys())[list(Teams.keys()).index(name)-1]]
            Teams.pop(name)
            tkm.showwarning(title="Csapat Törölve!",message=f"A {name} nevű csapat törlődött ")
            self.EditBtnClick()

    def EditTeam(self, name):
        self.ActiveTeam = Teams[name]
        self.addBtnClick("edit")

    def SaveActiveTeam(self):
        if self.TeamNameVar != "" and self.ActiveTeam.Name != self.TeamNameVar.get():
            try:
                Teams.pop(self.ActiveTeam.Name)
            except KeyError:
                pass
            self.ActiveTeam.Name = self.TeamNameVar.get()
            Teams.setdefault(self.ActiveTeam.Name, self.ActiveTeam)
        self.ActiveTeam.Formation = self.FormationVar.get()
        for key,val in self.TacticsVars.items():
            self.ActiveTeam.Tactics[key] = val.get()
        
    def CreatePlayer(self, pos):
        print(pos)
        self.CreatedPlayer.Name = self.PlayerNameVar.get()
        for key in self.CreatedPlayer.Stats.keys():
            self.CreatedPlayer.Stats[key] = int(self.StatVars[key].get())
        self.CreatedPlayer.Position = self.PlayerPosVar.get()
        self.ActiveTeam.Players[pos] = self.CreatedPlayer
        self.TeamFormationScreenBtn("edit")
        # for player in self.ActiveTeam.Players.values():
        #     print(player.Name)

    def GetNewTeamNum(self):
        num = 0
        for team in Teams.values():
            if "New Team(" in team.Name and int(team.Name[-2]) > num:
                num = int(team.Name[-2])
        return num + 1
if __name__ == "__main__":
    gui = GUI()
    print(Load(1))
    gui.mainloop()
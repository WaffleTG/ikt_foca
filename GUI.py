import random
import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk
import CTkMessagebox as ctkm
from Data import Teams, Formations, PosCords, LastTeam, currentSS, ChanceCountModes, TacticsKeys
from PIL import Image
from OtherFunctions import Save, Load, FormatPosition, OnStart, GenerateRandName, GetTeamIndexByName, GetIndexByPlayer, GetTeamGK
from Classes import Player, Team, Chance, Ref
import webbrowser
import copy
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GUI(ctk.CTk):
    def __init__(self, mode="") -> None:
        super().__init__()
        self.mode = mode
        self.SmallerButtonFont = ('Helvetica', 18, 'bold')
        self.ButtonFont = ('Helvetica', 26, 'bold')
        self.EntryFont = ('Helvetica', 20, 'bold')
        self.HeaderFont = ('Helvetica', 30, 'bold')
        self.BiggerHeaderFont = ('Helvetica', 42, 'bold')
        self.NormalFont = ('Helvetica', 24, 'bold')
        self.FormationFont = ('Helvetica', 16, 'bold')
        
        icon1 = tk.PhotoImage(file = 'Images/dice.png')
        self.iconphoto(True,icon1)

        self.SimNumFont = ('Helvetica', 100, 'bold')
        self.StatFont = ('Helvetica', 70, 'bold')
        self.SimTeamFont = ('Helvetica', 36, 'bold')
        self.ActiveTeam = LastTeam
        self.geometry("1100x580")
        self.title("Football Simulation")
        self.resizable(False, False)
        self.StartScreen()            
        self.bind_class('Entry', '<Control-BackSpace>', self.entry_ctrl_bs)
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
    def OnClose(self):
        if self.mode != "Dev":
            msgBox = ctkm.CTkMessagebox(title="Kilépés", message="Szeretnéd menteni a csapatokat?", option_1="Igen", option_2="Nem", option_3="Mégsem")
            match msgBox.get():
                case "Igen":
                    Save(currentSS)
                case "Nem":
                    pass
                case _:
                    return
            
            
        self.destroy()
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
        self.BackBtn.pack(side=tk.BOTTOM, padx=20, anchor="w", pady=10)
        
    def StartScreen(self):
        self.clearWindow()
        self.PlayBtn = ctk.CTkButton(self, 400, 80, text="Játék Számítógép ellen", font=self.ButtonFont, command=self.GameVsAi)
        self.PlayBtn.pack(pady=30)
        if len(Teams)>0:
            self.PlayBtn.configure(state="normal")

        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapatok szerkesztése", font=self.ButtonFont, command=self.EditBtnClick)
        self.EditBtn.pack(pady=0)
        
        self.SpecialModeBtn = ctk.CTkButton(self, 400, 80, text="Random Csapat Generálása", font=self.ButtonFont, command=self.GenerateRandomTeam)
        self.SpecialModeBtn.pack(pady=(30,0))

        self.LoadSaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés betöltése", font=self.ButtonFont, command=self.ChooseSaveSlot)
        self.LoadSaveBtn.pack(pady=30)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="About", font=self.ButtonFont, command=self.AboutClick)
        self.BackBtn.pack(side=tk.BOTTOM, padx=20, anchor="w", pady=10)
        self.button_image = ctk.CTkImage(Image.open("Images/dice.png"), size=(40, 40))
        # for i,team in enumerate(Teams.values()):
        #     print(f"Team {i} Name: {team.Name}")
        # try:
        #     print(f"ActiveTeamName: {self.ActiveTeam.Name}")
        # except:
        #     pass
        
        # 🎲⚅
    def AboutClick(self):
        webbrowser.open("https://waffletg.github.io/ikt_foca/")
    def GameVsAi(self):
        if len(Teams) == 0:
            tkm.showinfo(title="Nem Lehet Játékot Indítani!", message="Nincs egy csapat se elmentve!")
        else:
            self.clearWindow()
            self.GenerateReferee()
            self.RefeereVar = ctk.StringVar(value=self.Referees[0].Name)
            referees = [x.Name for x in self.Referees]
            self.columnconfigure((0,1,2,3), weight=1)
            self.rowconfigure((0,1,2,3,4,5), weight=0)
            try:
                if self.ActiveTeam.Name in Teams.keys():
                    self.team1Var.set(self.ActiveTeam.Name)
                else:
                    self.team1Var = ctk.StringVar(value=Teams[list(Teams.keys())[0]].Name)
            except AttributeError:
                self.team1Var = ctk.StringVar(value=Teams[list(Teams.keys())[0]].Name)
            
            self.team2Var = ctk.StringVar(value=Teams[list(Teams.keys())[0]].Name)
            
            # self.gameModeVar = ctk.StringVar(value=GameModes[0])
            self.ChanceCountVar = ctk.IntVar(value=10)
            self.GameLengthVar = ctk.IntVar(value=90)
            if len(Teams) > 1:
                self.team2Var.set(Teams[list(Teams.keys())[1]].Name)
            Teams[self.team1Var.get()].SetStats(0)
            Teams[self.team2Var.get()].SetStats(1)
            #1.Sor
            self.HeadLabel = ctk.CTkLabel(self,text="Válassz Csapatokat",font=self.HeaderFont).grid(column=0, columnspan=4, row=0, pady=(20,10))
            
            #2.Sor
            self.Team1Option = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.team1Var)
            self.Team1Option.grid(column=1, row=1, pady=20, padx=(15,0))
            self.Team2Option = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.team2Var).grid(column=2, row=1, pady=20, padx=(15,0))
            self.Rand1Button = ctk.CTkButton(self, 40, 40,image=self.button_image,text="",   command=lambda: self.RandomiseTeam(0)).grid(column=0, row=1, sticky="e")
            self.Rand2Button = ctk.CTkButton(self, 40, 40,image=self.button_image,text="" ,  command=lambda: self.RandomiseTeam(1)).grid(column=3, row=1, sticky="w")
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
            self.RefereeChoiceLabel = ctk.CTkLabel(self, font=self.EntryFont, text="Bíró").grid(column=1, row=6, pady=(20,0), sticky="w", padx=(55,0))
            self.ChanceCountChoiceLabel = ctk.CTkLabel(self, font=self.EntryFont, text="Helyzetek Száma").grid(column=2, row=6, pady=(20,0), sticky="w", padx=(55,0))
            
            self.RefereeChoice = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=referees, variable=self.RefeereVar).grid(column=1, row=7, pady=(0,30), padx=(15,0))
            self.ChanceCountChoice = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(ChanceCountModes.keys()), command=self.UpdateChanceCount).grid(column=2, row=7, pady=(0,30), padx=(15,0))
            #9-10.Sor
            self.GameLengthLabel = ctk.CTkLabel(self, font=self.EntryFont, text=f"Meccs Hossza: {self.GameLengthVar.get()} Perc")
            self.GameLengthLabel.grid(row=8,column=1, padx=(0,40))
            self.GameLengthSlider = ctk.CTkSlider(self, width=280, height=26,from_=30, to=180, number_of_steps=150,variable=self.GameLengthVar, command=self.UpdateLengthSlider).grid(row=9, column=1)
            #11.sor
            self.GameStartButton = ctk.CTkButton(self, 280, 40, text="Játék indítása", font=self.EntryFont, command=lambda:self.SimulationScreen(Teams[self.team1Var.get()], Teams[self.team2Var.get()],self.ChanceCountVar.get(), self.GameLengthVar.get())).grid(column=2, row=8, rowspan=2)
            #12.sor
            self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.StartScreen).grid(row=11, column=0, sticky="sw",pady=(91,0), padx=20)
    def GenerateReferee(self, amount: int=4):
        self.Referees = []
        with open('Datafiles/Referees.txt', 'r', encoding='utf-8') as f:
            NamesList = f.readlines()
            for i in range(amount):
                SplitName = random.choice(NamesList)
                NamesList.remove(SplitName)
                SplitName = SplitName.strip().split()
                Name = f"{SplitName[0]} {SplitName[1]}"
                self.Referees.append(Ref(int(SplitName[2]), int(SplitName[3]), Name))
    def UpdateChanceCount(self, *args):
        self.ChanceCountVar.set(ChanceCountModes[args[0]])
    def UpdateLengthSlider(self, *args):
        self.GameLengthLabel.configure(text=f"Meccs Hossza: {args[0]:.0f} Perc")
    def UpdateLabels(self, *args):
        try:
            team1 = Teams[self.team1Var.get()]
            team2 = Teams[self.team2Var.get()]
            team1.SetStats(GetTeamIndexByName(team1.Name))
            team2.SetStats(GetTeamIndexByName(team2.Name))
        except AttributeError:
            team1.SetStats(GetTeamIndexByName(team1.Name))
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
    def SimulationScreen(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90,firstTime=True):
        self.Referee = self.Referees[[x.Name for x in self.Referees].index(self.RefeereVar.get())]
        team1.SetStats(0)
        team2.SetStats(1)
        self.clearWindow()
        if firstTime:
            self.stops = []
            self.ScoreList = [0, 0]
            self.speedVar = ctk.IntVar(value=1)
            self.chances = self.GenerateSimulation(team1, team2, ChanceCount, MatchLength)[0] 
            self.CommentaryVar = ctk.StringVar(value="Meccs Kezdése?")
            self.timeVar = ctk.IntVar(value=0)
            self.ChancesList = [0,0]
            self.YellowCardList = [0,0]
            self.OffsideList = [0,0]
            self.RedCardList = [0,0]
            self.PossesionList = self.GeneratePosList(team1, team2)
        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1,3,4,5,6), weight=0)
        self.rowconfigure(2, weight=0)
        
        self.Score = ctk.StringVar(value=f"{self.ScoreList[0]} - {self.ScoreList[1]}")
        #első sor
        self.TimeLabel = ctk.CTkLabel(self, textvariable = self.timeVar, font=self.SimNumFont).grid(column=1,columnspan=3,row=0)
        self.StatButton = ctk.CTkButton(self, 40,40, text="Statisztika", font=self.EntryFont, command=lambda:self.ShowStat(team1, team2, ChanceCount, MatchLength)).grid(column=4, row=0)
        
        #második sor
        self.Team1Label = ctk.CTkLabel(self, text=team1.Name, font=self.SimTeamFont).grid(column=0 ,row=1, sticky="e")
        self.ScoreLabel = ctk.CTkLabel(self, textvariable = self.Score, font=self.SimNumFont).grid(column=1,columnspan=3,row=1)
        self.Team2Label = ctk.CTkLabel(self, text=team2.Name, font=self.SimTeamFont).grid(column=4 ,row=1, sticky="w")
        
        #harmadik sor
        self.CommentaryLabel = ctk.CTkLabel(self,width=900,height=150, anchor="nw",textvariable = self.CommentaryVar, font=self.EntryFont, bg_color="grey20", fg_color="grey20").grid(column=0, columnspan=5, row=2)
        # self.CommentaryBox = ctk.CTkFrame(self, width=900, height=150)
        # self.CommentaryBox.grid(column=0,columnspan=5 ,row=2)
        # self.CommentaryFrame = ctk.CTkFrame(self.CommentaryBox, width=900, height=150)
        # self.CommentaryFrame.pack(fill="both")
        # self.CommentaryLabel = ctk.CTkLabel(self.CommentaryFrame,width=900,height=150, textvariable = self.CommentaryVar, font=self.EntryFont).pack()
        
        #negyedik sor
        self.EndButton = ctk.CTkButton(self, 180,40, text="Mérkőzés Feladása", font=self.SmallerButtonFont,command=self.EndGame)
        self.EndButton.grid(column=0,row=3, padx=(73,0))
        self.StartButton = ctk.CTkButton(self, 180,40, text="Szimuláció indítása", font=self.SmallerButtonFont, command=lambda: self.StartSim(team1,team2, ChanceCount, MatchLength, self.timeVar.get()))
        self.StartButton.grid(column=1, row=3, pady=20)
        self.StopButton = ctk.CTkButton(self, 180,40, text="Szimuláció Megállítása", font=self.SmallerButtonFont, command=self.StopSim, state="disabled")
        self.StopButton.grid(column=2, row=3, pady=20)
        self.TacticsChangeButton = ctk.CTkButton(self, 180,40, text="Taktika Szerkesztése", font=self.SmallerButtonFont, command=lambda:self.addBtnClick("ingame", gameArgs={"team1":team1, "team2":team2, "ChanceCount": ChanceCount, "MatchLength": MatchLength}))
        self.TacticsChangeButton.grid(column=3,columnspan=2, row=3, pady=20, sticky="w", padx=(20,0))
        self.ActiveTeam = team1
        #Simulation
    def EndGame(self):
        pass
    def tksleep(self, time:float):
        self.after(int(time*1000), self.quit)
        self.mainloop()
    def StartSim(self, team1:Team,team2:Team, ChanceCount:int, MatchLength:int, Begin:int):
        self.run = True
        self.StartButton.configure(state="disabled")
        self.StopButton.configure(state="normal")
        
        for i in range(Begin+1,MatchLength+self.ExtraTime+1):
            if i != int(MatchLength/2+self.ExtraTime/3) +1:
                if self.run:
                    #Possession Chance On Start
                    self.timeVar.set(i)
                    team1.HandleFitness(MatchLength)
                    team2.HandleFitness(MatchLength)
                    try:
                        PosAmount = random.randint(0, i % 6)
                    except ValueError:
                        PosAmount = random.randint(0, 3)
                    randNum = random.randint(0, round((team1.MidOverall+team2.Overall)*100))
                    if (randNum < team2.MidOverall * self.PossesionList[0] and self.PossesionList[0] > 30) or self.PossesionList[1] < 30 :
                        self.PossesionList[0] -= PosAmount
                        self.PossesionList[1] += PosAmount
                    else:
                        self.PossesionList[0] += PosAmount
                        self.PossesionList[1] -= PosAmount
                    if i in self.chances.keys():
                        chance = self.chances[i]
                        if chance.Team.SimulationId == team1.SimulationId:
                            if chance.ChanceType == "Goal":
                                self.Goal(team1)
                            elif chance.ChanceType == "YellowCardChance":
                                self.YellowCard(team1, chance.Player)
                            elif chance.ChanceType == "RedCardChance":
                                self.RedCard(team1, chance.Player)
                            elif chance.ChanceType == "OffsideChance":
                                self.OffsideList[0] += 1
                            elif chance.ChanceType == "Penalty":
                                self.StopSim(False)
                                if self.Penalty(Taker=self.GenerateChancePlayerByAttribute(team1, "Attacking"), Keeper=GetTeamGK(team2)):
                                    self.Goal(team1)
                                    chance.ChanceType = "PenaltyGoal"
                                else:
                                    chance.ChanceType = "PenaltyMiss"
                                if "Penalty" not in chance.ChanceType:
                                    chance.GenerateComm()
                                    self.SimulationCommentator(chance)
                                self.StartSim(team1, team2, ChanceCount, MatchLength, self.timeVar.get())
                            else:
                                self.ChancesList[0] += 1
                        else:
                            if chance.ChanceType == "Goal":
                                self.Goal(team2)
                            elif chance.ChanceType == "YellowCardChance":
                                self.YellowCard(team2, chance.Player)
                            elif chance.ChanceType == "RedCardChance":
                                self.RedCard(team2, chance.Player)
                            elif chance.ChanceType == "OffsideChance":
                                self.OffsideList[1] += 1
                            elif chance.ChanceType == "Penalty":
                                self.StopSim(False)
                                if self.Penalty(Taker=self.GenerateChancePlayerByAttribute(team2, "Attacking"), Keeper=GetTeamGK(team1), Att=False):
                                    self.Goal(team2)
                                    chance.ChanceType = "PenaltyGoal"
                                else:
                                    chance.ChanceType = "PenaltyMiss"
                                chance.GenerateComm()
                                self.SimulationCommentator(chance)
                                self.StartSim(team1, team2, ChanceCount, MatchLength, self.timeVar.get())
                            else:
                                self.ChancesList[1] += 1
                        try:
                            if "Penalty" not in chance.ChanceType:
                                chance.GenerateComm()
                                self.SimulationCommentator(chance)
                        except KeyError:
                            print("Line360 Keyerror")
                        self.tksleep(1)
                        self.chances = self.GenerateSimulation(team1, team2, ChanceCount, MatchLength)[0]
                    self.Score.set(f"{self.ScoreList[0]} - {self.ScoreList[1]}")
                    self.tksleep(0.33/self.speedVar.get())
                else:
                    return
            else:
                #Félidő
                self.timeVar.set(i)
                self.SimulationCommentator(f"Félidő. A Játékosok {self.Score.get()} Állással mennek a szünetre.")
                self.StopSim()
    def Goal(self, team:Team):
        self.ChancesList[team.SimulationId] += 1
        self.ScoreList[team.SimulationId] += 1
    
    def YellowCard(self, team:Team, player:Player):
        if player.YellowCards > 0:
            self.RedCard(team, player)
        self.YellowCardList[team.SimulationId] += 1
        
    def Penalty(self,Taker:Player, Keeper:Player,Att:bool=True):
        self.StopSim(False)
        if Att:
            mess = f"Tizenegyest rúg a csapatod! Döntsd el a játékos merre rúgja!"
        else:
            mess = f"Az ellenfél tizenegyest rúg! Dönstd el merre vetődjön a kapusod"
        options = ["Jobbra","Középre","Balra"] 
        msg = ctkm.CTkMessagebox(title="Büntető", message=mess,
            icon="warning", option_1=options[0], option_2=options[1], option_3=options[2])
        randSide = random.choice(options)
        #1. Gólesély 2.Védésesély
        Chances = [0,0]
        Chances[0] += Taker.Stats["Attacking"]
        Chances[1] += Keeper.Stats["GoalKeeping"]
        Side = msg.get()
        if randSide == Side:
            Chances[1] *= 2        
        else:
            Chances[0] *= 8
        if random.choices(Chances, Chances, k=1)[0] == Chances[0]:
            return True
        return False
    def RedCard(self, team:Team, player:Player):
        team.Players.pop(list(team.Players.keys())[GetIndexByPlayer(team, player)])
        self.RedCardList[team.SimulationId] += 1
        team.SetStats(team.SimulationId)
        team.GetActivePlayers()
        if len(team.ActivePlayers) <= 6:
            self.StopSim(False)
            ctkm.CTkMessagebox(self, title="Mérkőzés Vége",icon="warning", message=f"A {team.Name} nevű csapat Játékosainak száma ezzel a piroslappal kevesebb, mint 7 főre csökkent, így kénytelenek voltak feladni a mérkőzést")
            self.SimulationCommentator(Chance(self.timeVar.get(), team, "MatchResignRedCard", random.choice(list(team.Players.values()))))
    def SimulationCommentator(self, chance:Chance):
        self.CommentaryVar.set("")
        try:
            lineLen = 0
            for x in chance.Comm:
                self.CommentaryVar.set(f"{self.CommentaryVar.get()}{x}")
                self.tksleep(0.05)
                lineLen += 1
                if lineLen > 80 and x == " ":
                    lineLen = 0
                    self.CommentaryVar.set(f"{self.CommentaryVar.get()}\n")
        except AttributeError:
            for x in chance:
                self.CommentaryVar.set(f"{self.CommentaryVar.get()}{x}")
                self.tksleep(0.05)

    def StopSim(self, SetButtons=True):
        self.run = False
        if SetButtons:
            self.StopButton.configure(state="disabled")
            self.StartButton.configure(state="normal")
        self.stops.append(self.timeVar.get())
    def ShowStat(self,team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90):
        self.StopSim()
        self.clearWindow()
        self.columnconfigure((0,2,4), weight=1)
        self.columnconfigure((1,3,5,6,7),weight=0)
        
        self.StatHeadLabel = ctk.CTkLabel(self, text="Statisztika", font=self.SimTeamFont).grid(column=1,row=0, columnspan=3, pady=5)
        #Közepe
        self.GoalLabel = ctk.CTkLabel(self, text=f"Gólok", font=self.SimTeamFont).grid(column=1,row=1, columnspan=3)
        self.ChanceLabel = ctk.CTkLabel(self, text=f"Helyzetek", font=self.SimTeamFont).grid(column=1,row=2, columnspan=3, pady=5)
        self.PossessionLabel = ctk.CTkLabel(self, text=f"Labdabirtoklás", font=self.SimTeamFont).grid(column=1,row=3, columnspan=3)
        self.YellowCardLabel = ctk.CTkLabel(self, text=f"Sárga Lapok", font=self.SimTeamFont).grid(column=1,row=4, columnspan=3, pady=5)
        self.RedCardLabel = ctk.CTkLabel(self, text=f"Piros Lapok", font=self.SimTeamFont).grid(column=1,row=5, columnspan=3, pady=5)
        #1 Team1 Statok
        self.Team1StatLabel = ctk.CTkLabel(self, text=team1.Name, font=self.HeaderFont).grid(column=0,row=0)
        self.Team1GoalStatLabel = ctk.CTkLabel(self, text=self.ScoreList[0], font=self.StatFont).grid(column=0,row=1, pady=5)
        self.Team1ChanceStatLabel = ctk.CTkLabel(self, text=self.ChancesList[0], font=self.StatFont).grid(column=0,row=2)
        self.Team1PossessionStatLabel = ctk.CTkLabel(self, text=f"{self.PossesionList[0]:.0f}%", font=self.StatFont).grid(column=0,row=3, pady=5)
        self.Team1YellowCardStatLabel = ctk.CTkLabel(self, text=self.YellowCardList[0], font=self.StatFont).grid(column=0,row=4, pady=5)
        self.Team1YellowCardStatLabel = ctk.CTkLabel(self, text=self.RedCardList[0], font=self.StatFont).grid(column=0,row=5, pady=5)
        #Team2 Statok
        self.Team2StatLabel = ctk.CTkLabel(self, text=team2.Name, font=self.HeaderFont).grid(column=4,row=0, pady=5)
        self.Team2GoalStatLabel = ctk.CTkLabel(self, text=self.ScoreList[1], font=self.StatFont).grid(column=4,row=1, pady=5)
        self.Team2ChanceStatLabel = ctk.CTkLabel(self, text=self.ChancesList[1], font=self.StatFont).grid(column=4,row=2)
        self.Team2PossessionStatLabel = ctk.CTkLabel(self, text=f"{self.PossesionList[1]:.0f}%", font=self.StatFont).grid(column=4,row=3, pady=5)
        self.Team2YellowCardStatLabel = ctk.CTkLabel(self, text=self.YellowCardList[1], font=self.StatFont).grid(column=4,row=4, pady=5)
        self.Team2YellowCardStatLabel = ctk.CTkLabel(self, text=self.RedCardList[1], font=self.StatFont).grid(column=4,row=5, pady=5)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=lambda:self.SimulationScreen(team1, team2, ChanceCount, MatchLength, False)).grid(column=0, row=6, pady=10)
    def GeneratePosList(self, team1: Team, team2: Team):

        ovr1 = team1.AttOverall + team1.MidOverall * 2 + team1.DefOverall
        ovr2 = team2.AttOverall + team2.MidOverall * 2 + team2.DefOverall
        rand1 = random.randint(0, int((ovr1 + ovr2)/(ovr2/ovr1)))
        rand2 = random.randint(0, int((ovr1 + ovr2)/(ovr1/ovr2)))
        ovr1 += rand1
        ovr2 += rand2
        Posses = [ovr1 / ((ovr1 + ovr2)/100), ovr2 / ((ovr1 + ovr2)/100)]
        if Posses[0] < 20:
            Posses[0] += 20
            Posses[1] -= 20
        elif Posses[1] < 20:
            Posses[1] += 20
            Posses[0] -= 20
        return Posses

    def GenerateSimulation(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90):
        team1 = copy.copy(team1)
        team2 = copy.copy(team2)
        team1.SetStats(0)
        team2.SetStats(1)
        team1.GetActivePlayers()
        team2.GetActivePlayers()
        Chances = {}
        for i in range(1, int(ChanceCount)+2):
            AttTeam = random.randint(0, int(team1.MidOverall + team2.MidOverall))
            if AttTeam < team1.MidOverall /100 * 95:
                AttTeam = team1
                DefTeam = team2
                
            elif AttTeam < (team1.MidOverall + team2.MidOverall) / 100 * 95:
                AttTeam = team2
                DefTeam = team1
            else:
                continue
            
            ChanceTime = random.randint((i-1) * int(MatchLength/ChanceCount) + 1 ,((i) * int(MatchLength/ChanceCount)))
            chanceTypes = {
                "LongShotChance": int(AttTeam.Tactics["Shootrate"] + AttTeam.Tactics["Agressivness"]/4),
                "BigChance": int((1/AttTeam.Tactics["Attackspeed"]*100 + AttTeam.getTeamWork() + AttTeam.Tactics["Attackwidth"] + AttTeam.Tactics["Passlength"] + AttTeam.Tactics["Agressivness"]/2)/1.5),
                "YellowCardChance": int(AttTeam.Tactics["Agressivness"] + 10-self.Referee.Patience/10),
                "RedCardChance": int(AttTeam.Tactics["Agressivness"]/2 + 10-self.Referee.Patience/10),
                "OffsideChance": int(AttTeam.Tactics["Attackspeed"]/2),
                "Corner": int(AttTeam.Tactics["Attackspeed"] + AttTeam.Tactics["Attackwidth"]/2)
            }
            ChanceType = list(chanceTypes.keys())[list(chanceTypes.values()).index(random.choices(list(chanceTypes.values()), k=1, weights=list(chanceTypes.values()))[0])]
            match ChanceType:
                case "LongShotChance":
                    #Távoli Lövés Legnagyobb Lövés Statunak van a legnagyobb esélye lőni        
                    ChancePlayer = self.GenerateChancePlayerByAttribute(AttTeam, "Attacking")
                    GoalChance = random.randint(0, int(ChancePlayer.Stats["Attacking"] + GetTeamGK(DefTeam).Stats["GoalKeeping"]*4))
                    if GoalChance < ChancePlayer.Stats["Attacking"]:
                        ChanceType = "Goal"
                    elif GoalChance <int(ChancePlayer.Stats["Attacking"] + GetTeamGK(DefTeam).Stats["GoalKeeping"]*2):
                        ChanceType = "MissLongShot"
                    else:
                        ChanceType = "Corner"
                case "BigChance":
                    #Nagy Helyzet
                    ChancePlayer = self.GenerateBigChancePlayer(AttTeam)
                    Defender = self.GenerateChancePlayerByAttribute(DefTeam, "Defending")
                    GoalChance = random.randint(0, int((AttTeam.AttOverall+ChancePlayer.Stats["Attacking"]) /100 * 95) + int(DefTeam.DefOverall + Defender.Stats["Defending"]+100-self.Referee.Patience))
                    if GoalChance < (AttTeam.AttOverall+ChancePlayer.Stats["Attacking"])/100 * 95:
                        ChanceType = "Goal"
                    elif GoalChance < AttTeam.AttOverall+ChancePlayer.Stats["Attacking"] + DefTeam.DefOverall + Defender.Stats["Defending"]:
                        ChanceType = "NoBigChance"
                        pass
                    else:
                        ChanceType = "Penalty"

                    
                case "YellowCardChance":
                    #Sárgalap
                    ChancePlayer = self.GenerateChancePlayerByAttribute(AttTeam, "Agressivness")
                case "RedCardChance": 
                    #PirosLap
                    ChancePlayer = self.GenerateChancePlayerByAttribute(AttTeam, "Agressivness")
                case "OffsideChance":
                    #Les
                    MistakeChance = random.randint(1, 99)
                    if MistakeChance > self.Referee.Mistakes:
                        ChancePlayer = self.GenerateBigChancePlayer(AttTeam)
                        Defender = self.GenerateChancePlayerByAttribute(DefTeam, "Defending")
                        GoalChance = random.randint(0, int((AttTeam.AttOverall+ChancePlayer.Stats["Attacking"]) /100 * 95) + int(DefTeam.DefOverall + Defender.Stats["Defending"]+100-self.Referee.Patience))
                        if GoalChance < (AttTeam.AttOverall+ChancePlayer.Stats["Attacking"])/100 * 95:
                            ChanceType = "Goal"
                        elif GoalChance < AttTeam.AttOverall+ChancePlayer.Stats["Attacking"] + DefTeam.DefOverall + Defender.Stats["Defending"]:
                            ChanceType = "NoBigChance"
                            ChancePlayer = Defender
                            pass
                        else:
                            ChanceType = "Penalty"
                    else:
                        ChancePlayer = self.GenerateChancePlayerByAttribute(AttTeam, "Attacking")
            
            if ChanceType == "Corner":
                ChancePlayer = self.GenerateChancePlayerByAttribute(AttTeam, "Passing")
                DefPlayer = self.GenerateChancePlayerByAttribute(DefTeam, "Defending")
                ShotChance = random.randint(0, int(ChancePlayer.Stats["Passing"] + DefPlayer.Stats["Defending"]))
                if ShotChance > ChancePlayer.Stats["Attacking"]:
                    pass
                    ChancePlayer = DefPlayer
                else:
                    GoalChance = random.randint(0, int((AttTeam.AttOverall+ChancePlayer.Stats["Attacking"]) /100 * 95) + int(DefTeam.DefOverall + DefPlayer.Stats["Defending"]+100-self.Referee.Patience))
                    if GoalChance < (AttTeam.AttOverall+ChancePlayer.Stats["Attacking"])/100 * 95:
                        ChanceType = "Goal"
                    elif GoalChance < AttTeam.AttOverall+ChancePlayer.Stats["Attacking"] + DefTeam.DefOverall + DefPlayer.Stats["Defending"]:
                        pass
                    else:
                        ChanceType = "Penalty"

            Chance1 = Chance(ChanceTime, AttTeam, ChanceType, ChancePlayer)
            Chances.setdefault(ChanceTime, Chance1)
        golok = [0,0]
        for x in Chances.values():
            if x.ChanceType == "Goal":
                if x.Team.Name == team1.Name:
                    golok[0] += 1
                else:
                    golok[1] += 1
        self.ExtraTime = int(random.randint(1, int(MatchLength/ChanceCount))/2)+1
        return Chances, golok
    def SimTest(self, team1: Team, team2: Team, ChanceCount: int=10, MatchLength: int=90, simAmount=1000):
        ossz1Golok = 0 
        ossz2Golok = 0
        for i in range(0, simAmount):
            golok = self.GenerateSimulation(team1, team2, ChanceCount, MatchLength)[1]
            
            ossz1Golok += golok[0]
            ossz2Golok += golok[1]

        print(f"{ossz1Golok/simAmount} - {ossz2Golok/simAmount}")
    def GenerateBigChancePlayer(self, team: Team):
        
        while True:
            player1 = self.GenerateChancePlayerByAttribute(team, "Attacking")
            player2 = self.GenerateChancePlayerByAttribute(team, "Teamwork")
            if player1 == player2:
                return player1
    def GenerateChancePlayerByAttribute(self, team, attribute): 
        ActivePlayers = {key:player.Stats[attribute] for key,player in team.ActivePlayers.items()}
        return team.Players[list(ActivePlayers.keys())[list(ActivePlayers.values()).index(random.choices(list(ActivePlayers.values()), k=1, weights=list(ActivePlayers.values()))[0])]]
    def EditBtnClick(self):
        self.clearWindow()
        self.addBtn = ctk.CTkButton(self, 400, 80, text="Csapat Hozzáadása", font=self.ButtonFont, command=lambda: self.addBtnClick("add"))
        self.addBtn.pack(pady=30)

        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapat Szerkesztése", font=self.ButtonFont, command=lambda: self.ChooseTeam("edit"))
        self.EditBtn.pack(pady=0)

        self.DeleteBtn = ctk.CTkButton(self, 400, 80, text="Csapat Törlése", font=self.ButtonFont, command=lambda: self.ChooseTeam("delete"))
        self.DeleteBtn.pack(pady=30)

        self.SaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés", font=self.ButtonFont, command= lambda: Save(currentSS))
        self.SaveBtn.pack(pady=0)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.StartScreen)
        self.BackBtn.pack(side=tk.BOTTOM, padx=20, anchor="w", pady=10)

    def addBtnClick(self, mode, gameArgs:dict = {}):
        self.clearWindow()
        self.TacticsVars = {key: ctk.IntVar(value=50) for key in TacticsKeys}
        self.TeamNameVar = ctk.StringVar()
        self.FormationVar = ctk.StringVar(value="4-4-2")
       
        if mode == "add":
            # tacs = {}
            # for key in self.TacticsVars.keys():
            #     tacs.setdefault(key, 50)
            self.ActiveTeam = Team("", "", {key:50 for key in self.TacticsVars.keys()}, {})
        if mode == "edit" or mode =="ingame":
            
            for key, val in self.ActiveTeam.Tactics.items():
                self.TacticsVars[key].set(val)
            self.TeamNameVar.set(self.ActiveTeam.Name)
            self.FormationVar.set(self.ActiveTeam.Formation)
        

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
        self.AddPlayerButton = ctk.CTkButton(self,text="Csapat Szerkesztése",width=280, height=40, font=self.EntryFont, command=lambda:[self.TeamFormationScreenBtn(mode)])
        self.AddPlayerButton.grid(row=5, column=0,rowspan=2, padx=(xPadding,0), sticky="w", pady=(20,0))

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

        self.GenerateRandomTactics = ctk.CTkButton(self, 200, 40, text="Random Taktika Generálása", font=self.ButtonFont, command=self.RandomiseTacitcs).grid(row=11, column=1,columnspan=3, sticky="s", padx=xPadding)
        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.EditBtnClick)
        self.BackBtn.grid(row=11, column=0, sticky="w",pady=(127,0), padx=xPadding)
        self.SaveTeam = ctk.CTkButton(self, 120, 40, text="Mentés", font=self.ButtonFont, command=self.SaveActiveTeam).grid(row=11, column=4, sticky="sw", padx=xPadding)
        if mode == "ingame":
            self.BackBtn.configure(command=lambda:self.SimulationScreen(gameArgs["team1"], gameArgs["team2"], gameArgs["ChanceCount"], MatchLength=gameArgs["MatchLength"], firstTime=False))
            self.AddPlayerButton.configure(command=lambda:self.TeamFormationScreenBtn(mode, gameArgs))
    def GenRandTacs(self):
        tactics = {key: round((random.randint(10,100)/5))*5 for key in TacticsKeys}
        return tactics
    def RandomiseTacitcs(self):
        for key, val in self.GenRandTacs().items():
            self.TacticsVars[key].set(val)
    def GenerateRandomTeam(self):
        randomTeamNames = open("Datafiles/Teams.txt", "r", encoding="utf-8").readlines()
        teamName = random.choice(randomTeamNames).strip()
        teamFormation = random.choice(Formations)
        Tactics = self.GenRandTacs()
        self.ActiveTeam = Team(teamName, teamFormation, Tactics, {})
        
        Teams.setdefault(teamName, self.ActiveTeam)
        self.TeamFormationScreenBtn("rand")
    def DrawPitch(self):
        lineWidth = 3
        self.FormationFrame.create_line(260, 700, 260, 500, width=lineWidth,fill="white")
        self.FormationFrame.create_line(260, 500, 420, 500, width=lineWidth,fill="white")
        self.FormationFrame.create_line(420, 500, 420, 700, width=lineWidth,fill="white")
        self.FormationFrame.create_line(130, 700, 130, 400, width=lineWidth,fill="white")
        self.FormationFrame.create_line(130, 400, 550, 400, width=lineWidth,fill="white")
        self.FormationFrame.create_line(550, 400, 550, 700, width=lineWidth,fill="white")
        self.FormationFrame.create_arc(260, 350, 420, 450, width=lineWidth, start=0, extent=180, outline="white")
        self.FormationFrame.create_oval(336, 436, 344, 444, fill="white", outline="white")
        self.FormationFrame.create_line(0, 90, 700, 90, width=lineWidth,fill="white")
        self.FormationFrame.create_oval(260, 10, 420, 170, width=lineWidth, outline="white")
        self.FormationFrame.create_oval(336, 86, 344, 94, fill="white", outline="black")
    def TeamFormationScreenBtn(self, mode, gameArgs={}):
        self.clearWindow()
        self.NameVariables = {}
        if mode == "rand":
            for pos in PosCords.keys():
                self.NameVariables.setdefault(pos, ctk.StringVar(value=pos))
            for key in self.NameVariables:
                newkey = FormatPosition(key)
                while newkey == "SUB" or newkey == "RES":
                    newkey = FormatPosition(random.choice(list(PosCords.keys())))
                player = self.RandomisePlayerStats(newkey, True)
                self.ActiveTeam.Players.setdefault(key, player)
                self.NameVariables[key].set(player.Name.strip().split()[0])
                self.TacticsVars =  {key:ctk.IntVar(value=val) for key,val in self.ActiveTeam.Tactics.items()}
            try:
                self.FormationVar.set(self.ActiveTeam.Formation)
                self.TeamNameVar.set(self.ActiveTeam.Name)
            except AttributeError:
                self.FormationVar = ctk.StringVar(value=self.ActiveTeam.Formation)
                self.TeamNameVar = ctk.StringVar(value=self.ActiveTeam.Name)
        else:
            if mode == "edit" or mode == "ingame":
                self.ActiveTeam.Name = self.TeamNameVar.get()
                pass
            for key, val in self.TacticsVars.items():
                self.ActiveTeam.Tactics[key] = val.get()
            for pos in PosCords.keys():
                self.NameVariables.setdefault(pos, ctk.StringVar(value=pos))
            try:
                for key, val in self.ActiveTeam.Players.items():
                    names = val.Name.strip().split()
                    self.NameVariables[key] = ctk.StringVar(value=names[0]) if len(names[0]) >= 4 else ctk.StringVar(value=names[1]) 
            except AttributeError:
                pass
            if mode == "add":
                if self.TeamNameVar.get().strip() != "":
                    self.ActiveTeam.Name = self.TeamNameVar.get()
                else:
                    self.ActiveTeam.Name = f"Új Csapat({self.GetNewTeamNum()})"
                Teams.setdefault(self.ActiveTeam.Name, self.ActiveTeam)
                # #addteam
                # self.ActiveTeam = Team(self.TeamNameVar.get(), self.FormationVar.get(), tactics=self.Tactics, players={})
                # Teams[self.ActiveTeam.Name]= self.ActiveTeam
                # if mode == "edit":
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

        self.FormationFrame = ctk.CTkCanvas(self, width=700,height=580, bg="green",highlightthickness=0)
        self.FormationFrame.grid(row=0, column=2,rowspan=5, sticky="e")
        self.DrawPitch()
        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=lambda: self.addBtnClick("edit"))
        self.BackBtn.grid(row=3, column=0, sticky="sw", padx=20, pady=(90,0))
        if mode == "ingame":
            self.BackBtn.configure(command=lambda:self.addBtnClick(mode, gameArgs))
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
        try:
            if event.widget.cget('cursor') == self.LabelCursor:
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
                    self.NameVariables[W1Pos].set(self.ActiveTeam.Players[W1Pos].Name.strip().split()[0])
                    self.NameVariables[W2Pos].set(self.ActiveTeam.Players[W2Pos].Name.strip().split()[0])
                else:
                    self.ActiveTeam.Players.setdefault(W2Pos, self.ActiveTeam.Players[W1Pos])
                    self.ActiveTeam.Players.pop(W1Pos)
                    self.NameVariables[W2Pos].set(self.ActiveTeam.Players[W2Pos].Name.strip().split()[0]) 
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
    def FormatPlayerList(self):
        PlayerPositions = []
        for posititon in self.NameVariables.keys():
            PlayerPositions.append(FormatPosition(posititon))
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
        return PlayerPositions
    def CreatePlayerBtn(self, pos):
        self.clearWindow()
        PlayerPositions = self.FormatPlayerList()
        self.PlayerNameVar = ctk.StringVar()
        self.PlayerPosVar = ctk.StringVar(value=FormatPosition(pos)) if "RES" not in pos and "SUB" not in pos else ctk.StringVar(value=random.choice(PlayerPositions))    
        # try:
        #     self.PlayerPosVar = ctk.StringVar(value=self.ActiveTeam.Players[FormatPosition(pos)].Position)
        # except KeyError:
        #     if pos in PlayerPositions:
        #         self.PlayerPosVar = ctk.StringVar(value=pos)
        #     else:
        #         self.PlayerPosVar = ctk.StringVar(value=PlayerPositions[-1])
        if self.NameVariables[pos].get() != pos:
            #Edit Player
            self.PlayerNameVar.set(self.ActiveTeam.Players[pos].Name)
            self.CreatedPlayer = self.ActiveTeam.Players[pos]
            self.PlayerPosVar.set(self.CreatedPlayer.Position)
            addBtnText = "Szerkesztés Befejezése"
        else:
            self.CreatedPlayer = Player(self.PlayerNameVar.get(), 50,50,50,50,50,50,50,50,pos)
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
        self.PaceSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98,variable=self.StatVars["Pace"]).grid(row=1, column=1, sticky="w")
        self.PassingVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Passing"], font=self.NormalFont).grid(row=1, column=3)
        self.PassingSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98, variable=self.StatVars["Passing"]).grid(row=1, column=4, sticky="w")

        self.Gap = ctk.CTkLabel(self.StatSetFrame, text="", font=self.NormalFont).grid(row=0, column=2, padx=50)
        self.PaceLabel = ctk.CTkLabel(self.StatSetFrame, text="Gyorsaság", font=self.NormalFont).grid(row=0, column=1)
        self.PassingLabel = ctk.CTkLabel(self.StatSetFrame, text="Passzolás", font=self.NormalFont).grid(row=0, column=4)
        self.SpaceLabel1 = ctk.CTkLabel(self.StatSetFrame, text="  ", font=self.NormalFont).grid(row=0, column=0, padx=(0,30))
        self.SpaceLabel2 = ctk.CTkLabel(self.StatSetFrame, text="  ", font=self.NormalFont).grid(row=0, column=3, padx=(30,0))

        self.ShotVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Attacking"], font=self.NormalFont).grid(row=3, column=0)
        self.ShotSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98,variable=self.StatVars["Attacking"]).grid(row=3, column=1, sticky="w")
        self.DefVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Defending"], font=self.NormalFont).grid(row=3, column=3)
        self.DefSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98, variable=self.StatVars["Defending"]).grid(row=3, column=4, sticky="w")

        self.ShotLabel = ctk.CTkLabel(self.StatSetFrame, text="Támadás", font=self.NormalFont).grid(row=2, column=1)
        self.DefLabel = ctk.CTkLabel(self.StatSetFrame, text="Védekezés", font=self.NormalFont).grid(row=2, column=4)

        self.TeamworkVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Teamwork"], font=self.NormalFont).grid(row=5, column=0)
        self.TeamworkSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98,variable=self.StatVars["Teamwork"]).grid(row=5, column=1, sticky="w")
        self.GoalkeeperVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["GoalKeeping"], font=self.NormalFont).grid(row=5, column=3)
        self.GoalkeeperSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98, variable=self.StatVars["GoalKeeping"]).grid(row=5, column=4, sticky="w")

        self.TeamworkLabel = ctk.CTkLabel(self.StatSetFrame, text="Csapatmunka", font=self.NormalFont).grid(row=4, column=1)
        self.GoalkeeperLabel = ctk.CTkLabel(self.StatSetFrame, text="Vetődés", font=self.NormalFont).grid(row=4, column=4)

        self.AgressivnessVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Agressivness"], font=self.NormalFont).grid(row=7, column=0)
        self.AgressivnessSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98,variable=self.StatVars["Agressivness"]).grid(row=7, column=1, sticky="w")
        self.StaminaVarLabel = ctk.CTkLabel(self.StatSetFrame, textvariable = self.StatVars["Stamina"], font=self.NormalFont).grid(row=7, column=3)
        self.StaminaSlider = ctk.CTkSlider(self.StatSetFrame, width=200, height=26,from_=1, to=99, number_of_steps=98, variable=self.StatVars["Stamina"]).grid(row=7, column=4, sticky="w")

        self.AgressivnessLabel = ctk.CTkLabel(self.StatSetFrame, text="Agresszivitás", font=self.NormalFont).grid(row=6, column=1)
        self.StaminaLabel = ctk.CTkLabel(self.StatSetFrame, text="Állóképesség", font=self.NormalFont).grid(row=6, column=4)
        self.RandomisePlayerStatsBtn = ctk.CTkButton(self, width=200,height=40, text="Játékos Randomizálása", font=self.ButtonFont, command=lambda:self.RandomisePlayerStats(self.PlayerPosVar.get())).grid(row=5, column=1,columnspan=2, padx=(20,0))
    
    def RandomisePlayerStats(self, pos, RandTeam=False):
        
        stat = {}
        if "L" in pos or "R" in pos:
            stat["Pace"] = (random.randint(60, 99))  
        else:
            stat["Pace"] = (random.randint(30,90))
        if "M" in pos:
            stat["Passing"] = (random.randint(60,99))    
            stat["Defending"] = (random.randint(30, 80))
            stat["Attacking"] = (random.randint(30,90))
        elif "ST" in pos or "W" in pos:
            stat["Passing"] = (random.randint(30,70))
            stat["Defending"] = (random.randint(30, 60))
            stat["Attacking"] = (random.randint(70, 99))
        else:
           stat["Passing"] = (random.randint(30, 70))
           stat["Defending"] = (random.randint(70,99))
           stat["Attacking"] = (random.randint(30, 60))
            
        if pos == "GK":
            for val in stat.values():
                val = (random.randint(10, 30))
            stat["GoalKeeping"] = (random.randint(60, 99))
        else:
            stat["GoalKeeping"] = (random.randint(10, 30))

        stat["Agressivness"] = (random.randint(40,90))  
        stat["Stamina"] = (random.randint(40,90))
        stat["Teamwork"] = (random.randint(40,90))
        
        if not RandTeam:
            for key, val in stat.items():
                self.StatVars[key].set(val)
        else:
            player = Player(GenerateRandName(), stat["Defending"], stat["Pace"], stat["Attacking"], stat["Passing"], stat["GoalKeeping"], stat["Teamwork"], stat["Stamina"], stat["Agressivness"], pos)
            return player

    def ChooseTeam(self, action):
        if len(Teams) == 0:
            ctkm.CTkMessagebox(title="Nem lehet szerkeszteni csapatot!", message="Nincs elmentve egy csapat sem!")
        else:
            self.clearWindow()
            if self.ActiveTeam == None:
                self.ActiveTeam = Teams[list(Teams.keys())[0]]
            try:
                if self.ActiveTeam.Name not in Teams.keys():
                    self.ActiveTeam = Teams[list(Teams.keys())[0]]
            except:
                self.ActiveTeam = Teams[list(Teams.keys())[0]]
            self.team1Var = ctk.StringVar(value=self.ActiveTeam.Name)
            
            self.HeadLabel = ctk.CTkLabel(self, text="Válaszd ki a csapatot amit ki szeretnél törölni", font=self.HeaderFont)
            self.HeadLabel.pack(pady=10)
            Teams[self.team1Var.get()].SetStats(GetTeamIndexByName(self.ActiveTeam.Name))
            self.TeamChoiceOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont, dropdown_font=self.EntryFont, values=list(Teams.keys()), variable=self.team1Var)
            self.TeamChoiceOption.pack(pady=10)
            
            self.Att1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Támadás: {Teams[self.team1Var.get()].AttOverall:.0f}")
            self.Att1Label.pack()
            #4.Sor
            self.Mid1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Középpálya: {Teams[self.team1Var.get()].MidOverall:.0f}")
            self.Mid1Label.pack()
            #5.Sor
            self.Def1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Védelem: {Teams[self.team1Var.get()].DefOverall:.0f}")
            self.Def1Label.pack()   
            #6.Sor
            self.TeamWork1Label = ctk.CTkLabel(self, font=self.EntryFont, text=f"Összhang: {Teams[self.team1Var.get()].getTeamWork():.0f}")
            self.TeamWork1Label.pack()

            self.team1Var.trace("w", lambda *args: self.UpdateLabels(args, 0))                
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
        msgBox = ctkm.CTkMessagebox(title="Csapat Törlése", message=f"Biztos vagy benne, hogy törölni szeretnéd a {name} nevű csapatot?", option_1="Nem", option_2="Igen", icon="question")
        # answer = tkm.askyesno(title="Csapat Törlése", message=f"Biztos vagy benne hogy törölni szeretnék a {name} nevű csapatot?")
        if msgBox.get() == "Igen":
            self.ActiveTeam = Teams[list(Teams.keys())[list(Teams.keys()).index(name)-1]]
            Teams.pop(name)
            self.EditBtnClick()
            ctkm.CTkMessagebox(title="Csapat Törölve", message=f"A {name} nevű csapat törölve lett!", icon="check")
            
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
        if self.PlayerNameVar.get().strip() == "":
            self.PlayerNameVar.set(f"Új{pos}")
        self.CreatedPlayer.Name = self.PlayerNameVar.get()
        for key in self.CreatedPlayer.Stats.keys():
            self.CreatedPlayer.Stats[key] = int(self.StatVars[key].get())
        self.CreatedPlayer.Position = self.PlayerPosVar.get()
        self.ActiveTeam.Players[pos] = self.CreatedPlayer
        self.TeamFormationScreenBtn("edit")
    
 
    def GetNewTeamNum(self):
        num = 0
        for team in Teams.values():
            if "New Team(" in team.Name and int(team.Name[-2]) > num:
                num = int(team.Name[-2])
        return num + 1
if __name__ == "__main__":
    OnStart(" Development")
    gui = GUI("Dev")
    print(Load(1))
    gui.mainloop()
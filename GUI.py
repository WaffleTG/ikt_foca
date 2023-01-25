import tkinter as tk
import customtkinter as ctk
from Data import Formations, PosCords, LastSave, LastTeam
from OtherFunctions import Save, Load
from Classes import Player, Team

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.NameVariables = {}
        for pos in PosCords.keys():
            self.NameVariables.setdefault(pos, ctk.StringVar(value=pos))
        self.ButtonFont = ('Helvetica', 26, 'bold')
        self.EntryFont = ('Helvetica', 20, 'bold')
        self.HeaderFont = ('Helvetica', 30, 'bold')
        self.NormalFont = ('Helvetica', 24, 'bold')
        self.FormationFont = ('Helvetica', 16, 'bold')

        self.ActiveSave = LastSave
        self.ActiveTeam = LastTeam
        self.geometry("1100x580")
        self.title("Football Simulation")
        self.resizable(False, False)
        self.StartScreen()
               

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.unbind_all('<Button-1>')

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

    def StartScreen(self):
        self.clearWindow()
        self.PlayBtn = ctk.CTkButton(self, 400, 80, text="Játék Számítógép ellen", font=self.ButtonFont, command=self.clearWindow)
        self.PlayBtn.pack(pady=30)
        
        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapatok szerkesztése", font=self.ButtonFont, command=self.EditBtnClick)
        self.EditBtn.pack(pady=0)
        
        self.SpecialModeBtn = ctk.CTkButton(self, 400, 80, text="Speciális játékmód", font=self.ButtonFont, command=self.clearWindow)
        self.SpecialModeBtn.pack(pady=(30,0))

        self.LoadSaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés betöltése", font=self.ButtonFont, command=self.ChooseSaveSlot)
        self.LoadSaveBtn.pack(pady=30)

    def EditBtnClick(self):
        self.clearWindow()
        self.addBtn = ctk.CTkButton(self, 400, 80, text="Csapat Hozzáadása", font=self.ButtonFont, command=self.addBtnClick)
        self.addBtn.pack(pady=30)

        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapat Szerkesztése", font=self.ButtonFont, command=self.clearWindow)
        self.EditBtn.pack(pady=0)

        self.DeleteBtn = ctk.CTkButton(self, 400, 80, text="Csapat Törlése", font=self.ButtonFont, command=self.clearWindow)
        self.DeleteBtn.pack(pady=30)

        self.SaveBtn = ctk.CTkButton(self, 400, 80, text="Mentés", font=self.ButtonFont, command=Save)
        self.SaveBtn.pack(pady=0)

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.StartScreen)
        self.BackBtn.pack(side=tk.BOTTOM, padx=10, anchor="w", pady=10)

    def addBtnClick(self):
        
        self.clearWindow()
        self.TeamNameVar = ctk.StringVar()
        self.FormationVar = ctk.StringVar()
        self.DefWidthVar = ctk.IntVar()
        self.AttackWidthVar = ctk.IntVar()
        self.DefLineVar = ctk.IntVar()
        self.PassLengthVar = ctk.IntVar()
        self.AgressivnessVar = ctk.IntVar()
        self.AttackSpeedVar = ctk.IntVar()
        self.DefStyleVar = ctk.IntVar()
        self.ShootRateVar = ctk.IntVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        xPadding = 20
        self.HeaderLabel = ctk.CTkLabel(self, font=self.HeaderFont, text="Csapat Hozzáadása").grid(row=0, column=0, columnspan=5, pady=(10,30))

        self.NameLabel = ctk.CTkLabel(self, text="Csapat Név", font=self.EntryFont).grid(row=1, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
        self.NameEntry = ctk.CTkEntry(self, font=self.EntryFont, width=280, height=40, textvariable=self.TeamNameVar).grid(row=2, column=0 ,padx=(xPadding,0), sticky="w")
        
        self.FormationLabel = ctk.CTkLabel(self, text="Felállás", font=self.EntryFont).grid(row=3, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
        self.FormationOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont,dropdown_font=self.EntryFont, values=Formations, variable=self.FormationVar).grid(row=4, column=0, padx=(xPadding,0), sticky="w")

        self.AddPlayerButton = ctk.CTkButton(self,text="Játékos Hozzáadása",width=280, height=40, font=self.EntryFont, command=self.TeamFormationScreenBtn).grid(row=5, column=0,rowspan=2, padx=(xPadding,0), sticky="w", pady=(20,0))

        self.TacticsLabel = ctk.CTkLabel(self, text="Taktika", font=self.HeaderFont).grid(row=1, column=1, columnspan=4)
        
        self.DefendseLabel = ctk.CTkLabel(self, text="Védekezés", font=self.NormalFont).grid(row=2, column=1,columnspan=2)
        self.AttackLabel = ctk.CTkLabel(self, text="Támadás", font=self.NormalFont).grid(row=2, column=3, columnspan=2)

        self.DefWidthLabel = ctk.CTkLabel(self, text="Szélesség", font=self.EntryFont).grid(row=3, column=1, columnspan=2)
        self.AttackWidthLabel = ctk.CTkLabel(self, text="Szélesség", font=self.EntryFont).grid(row=3, column=3, columnspan=2)

        self.DefWidthVarLabel = ctk.CTkLabel(self, textvariable = self.DefWidthVar, font=self.EntryFont).grid(row=4, column=1, sticky="e",padx=10)
        self.DefWidthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.DefWidthVar).grid(row=4, column=2, sticky="w", padx=(0,40))
        self.AttackWidthVarLabel = ctk.CTkLabel(self, textvariable = self.AttackWidthVar, font=self.EntryFont).grid(row=4, column=3, sticky="e",padx=10)
        self.AttackWidthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.AttackWidthVar).grid(row=4, column=4, sticky="w", padx=(0,40))

        self.DefLineLabel = ctk.CTkLabel(self, text="Védővonal", font=self.EntryFont).grid(row=5, column=1, columnspan=2)
        self.PassLengthLabel = ctk.CTkLabel(self, text="Passzok Hossza", font=self.EntryFont).grid(row=5, column=3, columnspan=2)

        self.DefLineVarLabel = ctk.CTkLabel(self, textvariable = self.DefLineVar, font=self.EntryFont).grid(row=6, column=1, sticky="e",padx=10)
        self.DefLineSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.DefLineVar).grid(row=6, column=2, sticky="w", padx=(0,40))
        self.PassLengthVarLabel = ctk.CTkLabel(self, textvariable = self.PassLengthVar, font=self.EntryFont).grid(row=6, column=3, sticky="e",padx=10)
        self.PassLengthSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.PassLengthVar).grid(row=6, column=4, sticky="w", padx=(0,40))
        
        self.AgressivnessLabel = ctk.CTkLabel(self, text="Agresszivitás", font=self.EntryFont).grid(row=7, column=1, columnspan=2)
        self.AttackSpeedLabel = ctk.CTkLabel(self, text="Gyorsaság", font=self.EntryFont).grid(row=7, column=3, columnspan=2)

        self.AgressivnessVarLabel = ctk.CTkLabel(self, textvariable = self.AgressivnessVar, font=self.EntryFont).grid(row=8, column=1, sticky="e",padx=10)
        self.AgressivnessSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.AgressivnessVar).grid(row=8, column=2, sticky="w", padx=(0,40))
        self.AttackSpeedVarLabel = ctk.CTkLabel(self, textvariable = self.AttackSpeedVar, font=self.EntryFont).grid(row=8, column=3, sticky="e",padx=10)
        self.AttackSpeedSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.AttackSpeedVar).grid(row=8, column=4, sticky="w", padx=(0,40))

        self.DefStyleLabel = ctk.CTkLabel(self, text="Emberfogás", font=self.EntryFont).grid(row=9, column=1, columnspan=2)
        self.ShootRateLabel = ctk.CTkLabel(self, text="Lövésgyakoriság", font=self.EntryFont).grid(row=9, column=3, columnspan=2)

        self.DefStyleVarLabel = ctk.CTkLabel(self, textvariable = self.DefStyleVar, font=self.EntryFont).grid(row=10, column=1, sticky="e",padx=10)
        self.DefStyleSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100,variable=self.DefStyleVar).grid(row=10, column=2, sticky="w", padx=(0,40))
        self.ShootRateVarLabel = ctk.CTkLabel(self, textvariable = self.ShootRateVar, font=self.EntryFont).grid(row=10, column=3, sticky="e",padx=10)
        self.ShootRateSlider = ctk.CTkSlider(self, width=200, height=26,from_=0, to=100, number_of_steps=100, variable=self.ShootRateVar).grid(row=10, column=4, sticky="w", padx=(0,40))

        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.EditBtnClick).grid(row=11, column=0, sticky="w", pady=(120,0), padx=xPadding)
                 
    def TeamFormationScreenBtn(self):
        self.clearWindow()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=4)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

        LabelBgColor = "dark green"
        self.LabelCursor = "circle"
        self.ReserveLabel = ctk.CTkLabel(self,text="Tartalékok", font=self.HeaderFont).grid(row=0, column=0, sticky="s", pady=5)
        self.ReserveListoBox = tk.Listbox(self,background="dark slate grey", width=30, height=20).grid(row=1,column=0, sticky="nw", padx=(10,5))  
        self.ReserveAddButton = ctk.CTkButton(self, width=160,height=30, text="+", font=('Helvetica', 40, 'bold'), command=lambda: self.CreatePlayerBtn("Res"))
        self.ReserveAddButton.grid(row=2, column=0, sticky="n", pady="15")
        self.SubLabel = ctk.CTkLabel(self,text="Cserék", font=self.HeaderFont).grid(row=0, column=1, sticky="s", pady=5)
        self.SubListBox = tk.Listbox(self,background="dark slate grey", width=30, height=20).grid(row=1, column=1, sticky="nw", padx=(5,10))
        self.SubAddButton = ctk.CTkButton(self, width=160,text="+", font=('Helvetica', 40, 'bold'), command=lambda: self.CreatePlayerBtn("Sub"))
        self.SubAddButton.grid(row=2, column=1, sticky="n", pady="15")
        self.BackBtn = ctk.CTkButton(self, 120, 40, text="Vissza", font=self.ButtonFont, command=self.addBtnClick).grid(row=3, column=0, sticky="nw", padx=20)
        self.FormationFrame = ctk.CTkFrame(self, width=700,height=580, fg_color="green")
        self.FormationFrame.grid(row=0, column=2,rowspan=5, sticky="e")

        self.GKLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["GK"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor)
        self.GKLabel.place(x=PosCords["GK"][0], y=PosCords["GK"][1])
        self.CB1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CB1"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB1"][0],y=PosCords["CB1"][1])
        self.CB2Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CB2"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB2"][0],y=PosCords["CB2"][1])
        self.CM1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM1"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CM1"][0], y=PosCords["CM2"][1])
        self.CM2Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM2"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CM2"][0], y=PosCords["CM2"][1])
        if self.FormationVar.get() == "3-5-2":  
            self.CB3Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CM2"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CB3"][0],y=PosCords["CB3"][1])
        else:
            self.LBLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LB"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LB"][0], y=PosCords["LB"][1])
            self.RBLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RB"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RB"][0], y=PosCords["RB"][1])
        
        if self.FormationVar.get() != "4-4-2":
            self.CAMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["CAM"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["CAM"][0], y=PosCords["CAM"][1])
         
        if self.FormationVar.get() == "4-3-3":
            self.LWLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LW"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LW"][0], y=PosCords["LW"][1])
            self.RWLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RW"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RW"][0], y=PosCords["RW"][1])
            self.STLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["ST"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["ST"][0], y=PosCords["ST"][1])
        elif self.FormationVar.get() == "4-2-3-1":
            self.WAM2abel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["WAM2"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["WAM1"][0], y=PosCords["WAM1"][1])
            self.WAM1Label = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["WAM1"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["WAM2"][0], y=PosCords["WAM2"][1])
            self.STLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["ST"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["ST"][0], y=PosCords["ST"][1])
        else:
            self.LMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LM"],font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LM"][0], y=PosCords["LM"][1])
            self.RMLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RM"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RM"][0], y=PosCords["RM"][1])
            self.LSTLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["LST"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["LST"][0], y=PosCords["LST"][1])
            self.RSTLabel = ctk.CTkLabel(self.FormationFrame, textvariable = self.NameVariables["RST"], font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor, cursor=self.LabelCursor).place(x=PosCords["RST"][0], y=PosCords["RST"][1])

        self.FormationFrame.bind_class('Label', "<Button-1>", self.FormationLabelClick)
        
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

                    self.FormationFrame.bind_class('Label', '<Button-1>', lambda a=event.widget:self.PlayerSwitchByName(self, a), add=False)
        except AttributeError:
            pass
        
    def PlayerSwitchByName(self, event, widget1):
        print("PlayerSwitchByName")
        self.FormationFrame.bind_class('Label', '<Button-1>', self.FormationLabelClick, add=False)
              
    def GetPlayerPos(self, widget):
        xOffest = self.GKLabel.winfo_rootx() - PosCords["GK"][0]
        yOffset = self.GKLabel.winfo_rooty() - PosCords["GK"][1] + 4
        LabelPos = (widget.winfo_rootx() - xOffest, widget.winfo_rooty() - yOffset)
        return list(PosCords.keys())[list(PosCords.values()).index(LabelPos)]

    def CreatePlayerBtn(self, pos):
        self.clearWindow()
        self.CreatedPlayer = Player("", 0, 0, 0, 0,0 ,0,pos)
        self.PlayerNameVar = ctk.StringVar(value="Name")
        self.PlayerPosVar = ctk.StringVar(value=pos)
        self.StatVars = {}
        for key in self.CreatedPlayer.Stats.keys():
            self.StatVars.setdefault(key, ctk.IntVar())

        self.columnconfigure((0,1,2,3), weight=1)
        self.columnconfigure(4, weight=0)
        self.rowconfigure((0,1,2,3,4), weight=0)
        self.rowconfigure(5, weight=1)
  
        self.HeaderLabel = ctk.CTkLabel(self,text="Játékos Hozzáadása", font=self.HeaderFont).grid(row=0, column=0,columnspan=4, pady=(20,40))

        #column0
        self.PlayerNamLabel = ctk.CTkLabel(self,text="Player Name", font=self.NormalFont).grid(row=1, column=0, sticky="w", padx=(20,0))
        self.PlayerNameEntry = ctk.CTkEntry(self, font=self.EntryFont, width=280, height=40, textvariable=self.PlayerNameVar).grid(row=2, column=0, sticky="w", padx=(20,0), pady=(5,20))
        self.PlayerPosLabel = ctk.CTkLabel(self,text="Játékos Pozíciója", font=self.NormalFont).grid(row=3, column=0, sticky="w", padx=(20,0))
        self.PlayerPosOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont,dropdown_font=self.EntryFont, values=list(self.NameVariables.keys()), variable=self.PlayerPosVar).grid(row=4, column=0, sticky="w", padx=(20,0))
        self.AddButon = ctk.CTkButton(self, width=280,height=40, text="Hozzáadás", font=self.ButtonFont, command=self.CreatePlayer).grid(row=5, column=0, sticky="w", padx=(20,0))
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

    def CreatePlayer(self):
        pass
if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()


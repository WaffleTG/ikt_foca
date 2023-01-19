import tkinter as tk
import customtkinter as ctk
from Data import Formations, PosCords
from OtherFunctions import Save

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

        self.geometry("1100x580")
        self.title("Football Simulation")
        self.resizable(False, False)
        self.StartScreen()
       

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    def StartScreen(self):
        self.clearWindow()
        self.PlayBtn = ctk.CTkButton(self, 400, 80, text="Játék Számítógép ellen", font=self.ButtonFont, command=self.clearWindow)
        self.PlayBtn.pack(pady=30)
        
        self.EditBtn = ctk.CTkButton(self, 400, 80, text="Csapatok szerkesztése", font=self.ButtonFont, command=self.EditBtnClick)
        self.EditBtn.pack(pady=0)
        
        self.SpecialModeBtn = ctk.CTkButton(self, 400, 80, text="Speciális játékmód", font=self.ButtonFont, command=self.clearWindow)
        self.SpecialModeBtn.pack(pady=30)

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

        self.NameVar = ctk.StringVar()
        self.FormationVar = ctk.StringVar()
        self.DefWidthVar = ctk.IntVar()
        self.AttackWidthVar = ctk.IntVar()
        self.DefLineVar = ctk.IntVar()
        self.PassLengthVar = ctk.IntVar()
        self.AgressivnessVar = ctk.IntVar()
        self.AttackSpeedVar = ctk.IntVar()
        self.DefStyleVar = ctk.IntVar()
        self.ShootRateVar = ctk.IntVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        xPadding = 20
        self.HeaderLabel = ctk.CTkLabel(self, font=self.HeaderFont, text="Csapat Hozzáadása").grid(row=0, column=0, columnspan=5, pady=(10,30))

        self.NameLabel = ctk.CTkLabel(self, text="Csapat Név", font=self.EntryFont).grid(row=1, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
        self.NameEntry = ctk.CTkEntry(self, font=self.EntryFont, width=280, height=40, textvariable=self.NameVar).grid(row=2, column=0 ,padx=(xPadding,0), sticky="w")
        
        self.FormationLabel = ctk.CTkLabel(self, text="Felállás", font=self.EntryFont).grid(row=3, column=0, padx=(xPadding,0),sticky="w", pady=(10,0))
        self.FormationOption = ctk.CTkOptionMenu(self, width=280, height=40, font=self.EntryFont,dropdown_font=self.EntryFont, values=Formations, variable=self.FormationVar).grid(row=4, column=0, padx=(xPadding,0), sticky="w")

        self.AddPlayerButton = ctk.CTkButton(self,text="Játékos Hozzáadása",width=280, height=40, font=self.EntryFont, command=self.CreatePlayerBtn).grid(row=5, column=0,rowspan=2, padx=(xPadding,0), sticky="w", pady=(20,0))

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
                
        
    def CreatePlayerBtn(self):
        self.clearWindow()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=4)

        LabelBgColor = "dark green"

        self.ReverseListoBox = tk.Listbox(self,background="dark slate grey").grid(row=0,column=0, sticky="nw")  
        self.SubListBox = tk.Listbox(self,background="dark slate grey").grid(row=0, column=1, sticky="nw")
        self.FormationFrame = ctk.CTkFrame(self, width=580,height=580, fg_color="green").grid(row=0, column=2,rowspan=2, sticky="e")
        
        self.GKLabel = ctk.CTkLabel(self.FormationFrame, text="GK", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=PosCords["GK"][0], y=PosCords["GK"][1])
        self.CB1Label = ctk.CTkLabel(self.FormationFrame, text="CB1", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=900, y=470)
        self.CB2Label = ctk.CTkLabel(self.FormationFrame, text="CB2", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=700, y=470)
        self.LBLabel = ctk.CTkLabel(self.FormationFrame, text="LB", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=600, y=460)
        self.RBLabel = ctk.CTkLabel(self.FormationFrame, text="RB", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=1000, y=460)
        self.CDMLabel = ctk.CTkLabel(self.FormationFrame, text="CDM", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=800, y=400)
        self.CM1Label = ctk.CTkLabel(self.FormationFrame, text="CM1", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=900, y=350)
        self.CM2Label = ctk.CTkLabel(self.FormationFrame, text="CM2", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=700, y=350)
        self.LWLabel = ctk.CTkLabel(self.FormationFrame, text="LW", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=600, y=300)
        self.RWLabel = ctk.CTkLabel(self.FormationFrame, text="RW", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=1000, y=300)
        self.STLabel = ctk.CTkLabel(self.FormationFrame, text="ST", font=self.FormationFont, fg_color=LabelBgColor, bg_color=LabelBgColor).place(x=800, y=270)


        self.bind_class(ctk.CTkLabel, "<Button-1>", self.FormationLabelClick)

    def FormationLabelClick(self, event):
        print("clicked")
        

        

gui = GUI()
gui.CreatePlayerBtn()
gui.mainloop()


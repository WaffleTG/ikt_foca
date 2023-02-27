import GUI
from OtherFunctions import Load, OnStart

if __name__ == "__main__":
    OnStart()
    gui = GUI.GUI()
    Load(1)
    gui.mainloop()

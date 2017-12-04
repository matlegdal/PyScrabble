# from tkinter import *
from scrabble import *

# class Window(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.init_window()
#
#     def init_window(self):
#         self.master.title("Scrabble")
#
#         menu = Menu(self.master)
#         self.master.config(menu=menu)
#
#         fichiers = Menu(menu)
#         fichiers.add_command(label="Nouvelle partie")
#         fichiers.add_command(label="Sauvegarder la artie")
#         fichiers.add_command(label="Charger une partie")
#         fichiers.add_command(label="Quitter", command=exit)
#         menu.add_cascade(label="Fichiers", menu=fichiers)
#
#
#         aide = Menu(menu)
#         aide.add_command(label="Instructions")
#         menu.add_cascade(label="Aide", menu=aide)



root = Scrabble(2)
# root.geometry("800x600")
# Label(root, text="Bienvenue dans Scrabble!").grid()


root.mainloop()


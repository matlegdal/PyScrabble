from tkinter import *
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


root = Tk()
root.title("Scrabble")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

#menu déroulant

barre_menu = Menu(root)
menu1 = Menu(barre_menu, tearoff=0)
menu1.add_command(label="Nouvelle partie", state=DISABLED)  # TODO: commande de retourner à la fenêtre d'acceuil
menu1.add_command(label="Charger une partie", state=NORMAL) # TODO: commande qui ouvre une fenetre avec un text pour charger la partie
menu1.add_separator()
menu1.add_command(label="Quitter", command=root.quit)
barre_menu.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(barre_menu, tearoff=0)
menu2.add_command(label="Règlements")  # TODO: faire apparaître une fenêtre avec les règlements
barre_menu.add_cascade(label="Aide", menu=menu2)

root.config(menu=barre_menu)

# variable de pad
label_padx = 10
label_pady = 10

# message de bienvenue
Label(root, text="Bienvenue dans IFT-1004 Scrabble", font=("Times", 24),
      padx=label_padx, pady=label_pady).grid(row=0)
# label de la langue
Label(root, text="Choisissez la langue du jeu:", font=("Times", 16),
      padx=label_padx, pady=label_pady).grid(row=1)

# frame des choix de langues
cadre_choix_langue = Frame(root)
cadre_choix_langue.grid(row=2)

# radio button des langues dispo

root.radio_bouton_fr = Radiobutton(cadre_choix_langue, text='FR')
root.radio_bouton_en = Radiobutton(cadre_choix_langue, text='EN')

root.radio_bouton_fr.grid(column=0, row=0)
root.radio_bouton_en.grid(column=1, row=0)
root.radio_bouton_fr.flash()
root.radio_bouton_en.deselect()
#todo: faire apparaître les boutons déselectionnés

# radio button pour le nb de joueurs

Label(root, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=3)
# frame des choix de joueurs
cadre_choix_joueur = Frame(root)
cadre_choix_joueur.grid(row=4)

# radio button des choix du nb de joueurs

root.radio_bouton_2 = Radiobutton(cadre_choix_joueur, text='2 joueurs')
root.radio_bouton_3 = Radiobutton(cadre_choix_joueur, text='3 joueurs')
root.radio_bouton_4 = Radiobutton(cadre_choix_joueur, text='4 joueurs')
root.radio_bouton_computer = Radiobutton(cadre_choix_joueur, text='Jouer contre l\'ordinateur')
root.radio_bouton_2.grid(column=0, row=0)
root.radio_bouton_3.grid(column=1, row=0)
root.radio_bouton_4.grid(column=2, row=0)
root.radio_bouton_computer.grid(column=3, row=0)
# todo: faire apparaître les boutons déselectionnés

#frame du bouton commencer
cadre_bouton_commencer = Frame(root, padx=label_padx, pady=label_pady)
cadre_bouton_commencer.grid(row=5)
# bouton de commencer la partie

root.bouton_commencer = Button(cadre_bouton_commencer, text="Commencer la partie",
                               padx=label_padx, pady=label_pady)
root.bouton_commencer.grid(row=0)

# TODO cliquer sur commencer décolle Scrabble avec nb de joueurs sélectionnés et langue. ouvre aussi le plateau.





# root = Scrabble(2)
# root.geometry("800x600")
# Label(root, text="Bienvenue dans Scrabble!").grid()


root.mainloop()


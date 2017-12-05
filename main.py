from scrabble import *
# from tkinter.ttk import *
from math import floor



class App(Tk):

    # variable de pad
    label_padx = 10
    label_pady = 10

    def __init__(self):
        super().__init__()
        self.current = None
        self.plateau = None

        self.title("Scrabble")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # menu
        barre_menu = Menu(self)
        fichier = Menu(barre_menu, tearoff=0)
        fichier.add_command(label="Nouvelle partie", command=self.accueil)
        fichier.add_command(label="Sauvegarder la partie", state=DISABLED) # TODO: implanter sauvegarder_partie()
        fichier.add_command(label="Charger une partie", state=DISABLED)  # TODO: commande qui ouvre une fenetre avec un text pour charger la partie
        fichier.add_separator()
        fichier.add_command(label="Quitter", command=self.quit)
        barre_menu.add_cascade(label="Fichier", menu=fichier)

        aide = Menu(barre_menu, tearoff=0)
        aide.add_command(label="Règlements", state=DISABLED)  # TODO: faire apparaître une fenêtre avec les règlements
        barre_menu.add_cascade(label="Aide", menu=aide)

        self.config(menu=barre_menu)
        self.accueil()

    def accueil(self):
        if self.current is not None:
            self.current.destroy()

        if self.plateau is not None:
            self.plateau.destroy()


        self.current = Frame(self)
        self.current.grid(row=20)

        # message de bienvenue
        Label(self.current, text="Bienvenue dans IFT-1004 Scrabble", font=("Times", 24),
              # padx=App.label_padx, pady=App.label_pady
              ).grid(row=0)
        # label de la langue
        Label(self.current, text="Choisissez la langue du jeu:", font=("Times", 16),
              # padx=App.label_padx, pady=App.label_pady
              ).grid(row=1)

        # Choix des langues
        cadre_choix_langue = Frame(self.current)
        cadre_choix_langue.grid(row=2)
        langue = StringVar()
        Radiobutton(cadre_choix_langue, text='Français', variable=langue, value='FR').grid(column=0, row=0)
        Radiobutton(cadre_choix_langue, text='English', variable=langue, value='EN').grid(column=1, row=0)

        # Nombre des joueurs
        Label(self.current, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=3)
        cadre_choix_joueur = Frame(self.current)
        cadre_choix_joueur.grid(row=4)
        nb_joueurs = IntVar()
        Radiobutton(cadre_choix_joueur, text='2 joueurs', variable=nb_joueurs, value=2).grid(column=0, row=0)
        Radiobutton(cadre_choix_joueur, text='3 joueurs', variable=nb_joueurs, value=3).grid(column=1, row=0)
        Radiobutton(cadre_choix_joueur, text='4 joueurs', variable=nb_joueurs, value=4).grid(column=2, row=0)
        Radiobutton(cadre_choix_joueur, text='Jouer contre l\'ordinateur', variable=nb_joueurs, value=1, state=DISABLED).grid(column=3, row=0)


        # Débuter la partie
        cadre_bouton_commencer = Frame(self.current,
                                       # padx=App.label_padx, pady=App.label_pady
                                       )
        cadre_bouton_commencer.grid(row=5)

        self.current.bouton_commencer = Button(cadre_bouton_commencer, text="Commencer la partie", command=lambda: self.jouer(nb_joueurs.get(), langue.get()),
                                       # padx=App.label_padx, pady=App.label_pady
                                               )
        self.current.bouton_commencer.grid(row=0)


    def jouer(self, nb_joueurs, langue):
        self.current.destroy()

        self.current = Scrabble(self, nb_joueurs, langue)
        self.current.grid()

        # Plateau
        self.plateau = Plateau(self, 60)
        self.plateau.grid(row=0, column=0, sticky=NSEW)
        self.plateau.tag_bind('case', '<Button-1>', self.click_case)



    def click_case(self, event):
        ligne = floor(event.y/self.plateau.pixels_par_case)
        col = floor(event.x/self.plateau.pixels_par_case)

        print(event.x, event.y)
        print(ligne)
        print(col)
        print(self.plateau.cases[ligne][col])


# Style().theme_use('aqua')
App().mainloop()


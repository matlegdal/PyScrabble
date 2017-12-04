from scrabble import *
from math import floor


class Window(Tk):

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
              padx=Window.label_padx, pady=Window.label_pady).grid(row=0)
        # label de la langue
        Label(self.current, text="Choisissez la langue du jeu:", font=("Times", 16),
              padx=Window.label_padx, pady=Window.label_pady).grid(row=1)

        # frame des choix de langues
        cadre_choix_langue = Frame(self.current)
        cadre_choix_langue.grid(row=2)

        # radio button des langues dispo
        self.current.radio_bouton_fr = Radiobutton(cadre_choix_langue, text='FR')
        self.current.radio_bouton_en = Radiobutton(cadre_choix_langue, text='EN')

        self.current.radio_bouton_fr.grid(column=0, row=0)
        self.current.radio_bouton_en.grid(column=1, row=0)
        self.current.radio_bouton_fr.flash()
        self.current.radio_bouton_en.deselect()
        # todo: faire apparaître les boutons déselectionnés

        # radio button pour le nb de joueurs
        Label(self.current, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=3)
        # frame des choix de joueurs
        cadre_choix_joueur = Frame(self.current)
        cadre_choix_joueur.grid(row=4)

        # radio button des choix du nb de joueurs
        self.current.radio_bouton_2 = Radiobutton(cadre_choix_joueur, text='2 joueurs')
        self.current.radio_bouton_3 = Radiobutton(cadre_choix_joueur, text='3 joueurs')
        self.current.radio_bouton_4 = Radiobutton(cadre_choix_joueur, text='4 joueurs')
        self.current.radio_bouton_computer = Radiobutton(cadre_choix_joueur, text='Jouer contre l\'ordinateur')
        self.current.radio_bouton_2.grid(column=0, row=0)
        self.current.radio_bouton_3.grid(column=1, row=0)
        self.current.radio_bouton_4.grid(column=2, row=0)
        self.current.radio_bouton_computer.grid(column=3, row=0)
        # todo: faire apparaître les boutons déselectionnés

        # frame du bouton commencer
        cadre_bouton_commencer = Frame(self.current, padx=Window.label_padx, pady=Window.label_pady)
        cadre_bouton_commencer.grid(row=5)

        # bouton de commencer la partie
        self.current.bouton_commencer = Button(cadre_bouton_commencer, text="Commencer la partie", command=self.jouer,
                                       padx=Window.label_padx, pady=Window.label_pady)
        self.current.bouton_commencer.grid(row=0)

        # TODO cliquer sur commencer décolle Scrabble avec nb de joueurs sélectionnés et langue. ouvre aussi le plateau.

    def jouer(self, nb_joueurs=2, langue='fr'):
        self.current.destroy()

        self.current = Scrabble(self, nb_joueurs, langue)
        self.current.grid()

        # apparition du plateau
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








Window().mainloop()


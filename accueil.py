from tkinter import *


class Accueil(Frame):
    """
    Affichage de l'écran d'accueil.
    """

    PADX = 10
    PADY = 10

    def __init__(self, parent, root):
        super().__init__(parent)

        # Désactive les options nouvelle partie et sauvegarder partie du menu
        root.fichier.entryconfig(0, state="disabled")
        root.fichier.entryconfig(1, state="disabled")
        root.fichier.entryconfig(2, state="disabled")

        self.grid()

        # message de bienvenue
        Label(self, text="PyScrabble", font=("Times", 24)).grid(row=0, columnspan=5)
        # label de la langue
        Label(self, text="Choisissez la langue du jeu:", font=("Times", 16)).grid(row=1, column=0, sticky=E,
                                                                                     padx=self.PADX, pady=self.PADY)

        # Choix des langues
        langue = StringVar()
        langue.set('fr')
        Radiobutton(self, text='Français', variable=langue, value='fr').grid(row=1, column=1, sticky=W, pady=self.PADY)
        Radiobutton(self, text='English', variable=langue, value='en').grid(row=1, column=2, sticky=W, pady=self.PADY)

        # Nombre des joueurs
        Label(self, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=2, column=0, sticky=E,
                                                                                         padx=self.PADX, pady=self.PADY)
        nb_joueurs = IntVar()
        nb_joueurs.set(2)
        Radiobutton(self, text='2 joueurs', variable=nb_joueurs, value=2).grid(row=2, column=1, sticky=W, pady=self.PADY)
        Radiobutton(self, text='3 joueurs', variable=nb_joueurs, value=3).grid(row=2, column=2, sticky=W, pady=self.PADY)
        Radiobutton(self, text='4 joueurs', variable=nb_joueurs, value=4).grid(row=2, column=3, sticky=W, pady=self.PADY)
        Radiobutton(self, text='Jouer contre l\'ordinateur', variable=nb_joueurs, value=1, state=DISABLED).grid(row=2,
                                                                                                                   column=4,
                                                                                                                   sticky=W,
                                                                                                                   pady=self.PADY)

        # Difficulté
        Label(self, text="Choisissez la difficulté:", font=("Times", 16)).grid(row=3, column=0, sticky=E, padx=self.PADX,
                                                                                  pady=self.PADY)
        difficulte = StringVar()
        difficulte.set('facile')
        Radiobutton(self, text='Facile', variable=difficulte, value='facile').grid(row=3, column=1, sticky=W)
        Radiobutton(self, text='Règles officielles', variable=difficulte, value='difficile').grid(row=3, column=2,
                                                                                                     sticky=W)

        # Débuter la partie
        Button(self, text="Commencer une nouvelle partie",
               command=lambda: root.demarrer_partie(root, nb_joueurs.get(), langue.get(), difficulte.get())).grid(row=4,
                                                                                                                     column=1,
                                                                                                                     columnspan=2,
                                                                                                                     sticky=NSEW,
                                                                                                                     pady=self.PADY)
        Button(self, text="Charger une partie existante", command=root.charger_partie).grid(row=5, column=1,
                                                                                               columnspan=2, sticky=NSEW,
                                                                                                pady=self.PADY)
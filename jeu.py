from tkinter import *
from chevalet import Chevalet
from plateau import Plateau

class Jeu(Frame):

    PADX = 10
    PADY = 10

    def __init__(self, parent, root):
        super().__init__(parent)
        self.grid(row=0, column=0, rowspan=100, columnspan=100, sticky=NSEW)

        # Pointage
        pointage = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        pointage.grid(row=0, column=0, sticky=NSEW)
        pointage.grid_columnconfigure(0, weight=1)
        pointage.grid_columnconfigure(10, weight=1)

        for i in range(len(root.joueurs)):
            Label(pointage, text="{}".format(root.joueurs[i].nom)).grid(row=0, column=i+1, sticky=NSEW)
            points = Label(pointage, text="{}".format(root.joueurs[i].points))
            points.grid(row=1, column=i+1, sticky=NSEW)
            root.labels_points.append(points)


        # Message
        message = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        message.grid(row=0, column=1, sticky=NSEW)
        message.grid_columnconfigure(0, weight=1)
        message.grid_columnconfigure(10, weight=1)

        Label(message, textvariable=root.message).grid(row=0, column=1)

        # Compteur
        compteur = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        compteur.grid(row=1, column=1, sticky=NSEW)
        compteur.grid_columnconfigure(0, weight=1)
        compteur.grid_columnconfigure(10, weight=1)

        Label(compteur, text="Compteur").grid(row=0, column=1)
        root.temps_label = Label(compteur, text='0')
        root.temps_label.grid(row=2, column=1)

        # Timer
        self.timer = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        self.timer.grid(row=1, column=1, sticky=NSEW)
        self.timer.grid_columnconfigure(0, weight=1)
        self.timer.grid_columnconfigure(10, weight=1)

        Label(self.timer, text="Minuteur").grid(row=0, column=1)
        root.timer_label = Label(self.timer, text='')
        root.timer_label.grid(row=1, column=1)

        self.timer.lower()

        # joueur actif
        joueur = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        joueur.grid(row=2, column=1, sticky=NSEW)
        joueur.grid_columnconfigure(0, weight=1)
        joueur.grid_columnconfigure(10, weight=1)

        root.chevalet_actif = Chevalet(joueur, root.PIXELS_PAR_CASE)
        root.chevalet_actif.grid(row=0, column=1, columnspan=4, sticky=NS)

            # Boutons d'actions
        root.btn_jouer = Button(joueur, text="Jouer le tour", command=root.jouer_un_tour)
        root.btn_annuler = Button(joueur, text="Annuler", command=root.reprendre_tous_les_jetons)
        root.btn_passer = Button(joueur, text="Passer le tour", command=root.passer_un_tour)
        root.btn_changer = Button(joueur, text="Changer les jetons", command=root.demander_jetons_a_changer)
        root.btn_abandonner = Button(joueur, text="Abandonner", command=root.abandonner)

        root.btn_jouer.grid(row=1, column=1, columnspan=2, sticky=NSEW, pady=10)
        root.btn_annuler.grid(row=1, column=3, sticky=NSEW, pady=10)
        root.btn_passer.grid(row=2, column=1)
        root.btn_changer.grid(row=2, column=2)
        root.btn_abandonner.grid(row=2, column=3)

        # interface pour changer les jetons
        root.jeter = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        root.jeter.grid(row=3, column=1, sticky=NSEW)
        root.jeter.grid_columnconfigure(0, weight=1)
        root.jeter.grid_columnconfigure(10, weight=1)

        Label(root.jeter, text="Sélectionner les jetons à changer\net appuyez sur Confirmer").grid(row=0, column=1, columnspan=2)

        root.sac_a_jetons = Chevalet(root.jeter, root.PIXELS_PAR_CASE)
        root.sac_a_jetons.grid(row=1, column=1, columnspan=2, sticky=NS)

        Button(root.jeter, text="Confirmer", command=root.changer_jetons).grid(row=2, column=1, sticky=NSEW)
        Button(root.jeter, text="Cancel", command=root.annuler_changer_jetons).grid(row=2, column=2, sticky=NSEW)

        root.jeter.lower()

        # Interface d'assistance
        # todo: corriger le bug de redimensionnement
        assist = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        assist.grid(row=0, column=2, rowspan=2, sticky=NSEW)

        Label(assist, text="Suggestion de mots").pack()

        root.suggestions = Text(assist, width=40, height=10)
        root.suggestions.pack(side=LEFT, fill=BOTH, expand=YES, padx=self.PADX, pady=self.PADY)

        scroll_suggestions = Scrollbar(assist, command=root.suggestions.yview)
        scroll_suggestions.pack(side=RIGHT, fill=Y)

        root.suggestions.config(yscrollcommand=scroll_suggestions.set)

        # Historique
        # todo: redimensionnement
        log = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        log.grid(row=2, column=2, rowspan=3, sticky=NSEW)

        Label(log, text="Historique des tours").pack()

        root.log = Text(log, width=40, height=10)
        root.log.pack(side=LEFT, fill=BOTH, expand=YES, padx=self.PADX, pady=self.PADY)

        scroll_log = Scrollbar(log, command=root.log.yview)
        scroll_log.pack(side=RIGHT, fill=Y)

        root.log.config(yscrollcommand=scroll_log.set)

        root.log.insert(END, "Début de la partie.\n")
        root.log.config(state="disabled")




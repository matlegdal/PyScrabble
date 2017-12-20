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
        pointage.grid_columnconfigure(5, weight=1)

        for i in range(len(root.joueurs)):
            Label(pointage, text="{}".format(root.joueurs[i].nom)).grid(row=0, column=i+1, sticky=NSEW)
            points = Label(pointage, text="{}".format(root.joueurs[i].points))
            points.grid(row=1, column=i+1, sticky=NSEW)
            root.labels_points.append(points)


        # Message
        message = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        message.grid(row=0, column=1, sticky=NSEW)
        Label(message, textvariable=root.message).grid(row=0, column=0)

        # Compteur
        compteur = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        compteur.grid(row=1, column=1, sticky=NSEW)
        Label(compteur, text="Compteur").grid(row=0, column=0)

        # joueur actif
        joueur = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        joueur.grid(row=2, column=1, sticky=NSEW)
        root.chevalet_actif = Chevalet(joueur, root.PIXELS_PAR_CASE)
        root.chevalet_actif.grid(row=0, column=0, columnspan=4, sticky=NS)

            # Boutons d'actions
        root.btn_jouer = Button(joueur, text="Jouer le tour", command=root.jouer_un_tour)
        root.btn_annuler = Button(joueur, text="Annuler", command=root.reprendre_tous_les_jetons)
        root.btn_passer = Button(joueur, text="Passer le tour", command=root.passer_un_tour)
        root.btn_changer = Button(joueur, text="Changer les jetons", command=root.demander_jetons_a_changer)
        root.btn_abandonner = Button(joueur, text="Abandonner", command=root.abandonner)

        root.btn_jouer.grid(row=1, column=0, columnspan=2, sticky=NSEW, pady=10)
        root.btn_annuler.grid(row=1, column=2, sticky=NSEW, pady=10)
        root.btn_passer.grid(row=2, column=0)
        root.btn_changer.grid(row=2, column=1)
        root.btn_abandonner.grid(row=2, column=2)

        # interface pour changer les jetons
        jeter = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        jeter.grid(row=3, column=1, sticky=NSEW)

        Label(jeter, text="Sélectionner les jetons à changer\net appuyez sur Confirmer").grid(row=0, column=0, columnspan=2)

        root.sac_a_jetons = Chevalet(jeter, root.PIXELS_PAR_CASE)
        root.sac_a_jetons.grid(row=1, column=0, columnspan=2, sticky=NS)

        Button(jeter, text="Confirmer", command=root.changer_jetons).grid(row=2, column=0, sticky=NSEW)
        Button(jeter, text="Cancel", command=root.annuler_changer_jetons).grid(row=2, column=1, sticky=NSEW)

        # jeter.lower()

        # Interface d'assistance
        assist = Frame(parent, bd=1, relief="groove", padx=self.PADX, pady=self.PADY)
        assist.grid(row=0, column=2, rowspan=2, sticky=NSEW)

        Label(assist, text="Suggestion de mots").pack()

        text = Text(assist, width=20, height=10)
        text.pack(side=LEFT, fill=BOTH, expand=YES, padx=self.PADX, pady=self.PADY)

        scroll = Scrollbar(assist, command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)

        text.config(yscrollcommand=scroll.set)

        text.insert(END, "lorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum\nlorem\nipsum")

        text.config(state="disabled")



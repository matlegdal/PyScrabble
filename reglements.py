from tkinter import *

class Reglements(Toplevel):

    GENERALITES = """

Le Scrabble est un jeu de lettres qui se pratique à deux, trois ou quatre joueurs.

Le jeu consiste à former des mots entrecroisés sur une grille avec des lettres de valeurs différentes, les cases de 
couleur de la grille permettant de multiplier la valeur des lettres ou des mots. Le gagnant est celui qui cumule le plus
grand nombre de points à l'issue de la partie. Le jeu comporte 102 jetons (100 lettres et 2 jokers).

"""

    DEBUT = """
    
Chaque joueur pioche à tour de rôle une lettre dans le sac. Celui qui obtient la lettre la plus proche de A (dans
l’ordre alphabétique) joue en premier. Si plusieurs joueurs ont pioché la même lettre, ils posent leur lettre sur la 
table puis piochent chacun une nouvelle lettre dans le sac.

Si un joueur a pioché un joker (lettre blanche), il le pose sur la table puis pioche une nouvelle lettre dans le sac. 
Une fois le premier joueur déterminé, l’ordre des joueurs suit l'ordre normal croissant.

"""

    DEROULEMENT = """
    
Les joueurs jouent à tour de rôle.

Lorsque c’est son tour, un joueur pioche 7 pions dans le sac, puis il doit poser un mot d’au moins 2 lettres sur le 
plateau en utilisant un ou plusieurs de ses pions.

Une fois le mot posé, les points de ce mot sont ajoutés à son score (voir plus bas, « Décompte des points » ), et c’est 
au tour du joueur suivant.

Au début de la partie, le mot placé par le premier joueur doit obligatoirement passer par la case centrale, marquée
d’une étoile. Cette case faisant office de case « mot compte double », la valeur du mot posé est multipliée par deux.

Ensuite, chaque mot placé par un joueur doit obligatoirement se raccorder sur une ou plusieurs lettres déjà posées sur 
la grille.

Si un mot placé par un joueur forme d’autres mots, ceux-ci doivent également être des mots valides.

"""

    DECOMPTE = """
    
Lorsqu’un mot est placé sur le plateau, sa valeur est calculée comme suit : on additionne la somme des valeurs de chaque
lettre, en tenant compte des éventuelles cases « lettre compte double » ou « lettre compte triple » sur lesquelles 
sont posées ces lettres, puis on multiplie cette somme en tenant compte des éventuelles cases « mot compte double » ou 
« mot compte triple » sur lesquelles est posé ce mot.

Si le mot passe sur deux cases « mot compte double », sa valeur est multipliée par 4 (« quadruple »). Si le mot passe 
sur deux cases « mot compte triple », sa valeur est multipliée par 9 (« nonuple »).

Si le mot posé forme simultanément d’autres mots, la valeur de ces mots est également comptabilisée, puis on additionne 
la valeur de tous les mots formés. L’effet multiplicateur d’une case n’est pris en compte que pour le(s) mot(s) posé(s) 
en premier sur cette case.

Au coup suivant, seule la valeur de la lettre posée sur la case est prise en compte. Si un joueur utilise ses 7 pions 
pour former un mot, il a un bonus de 50 points. Chaque jeu de Scrabble possède 2 pions « blancs », ce sont les jokers.

Leur valeur est de 0 point, mais ils peuvent remplacer n’importe quelle lettre de l’alphabet, au choix du joueur. Ils 
permettent souvent de faire un « Scrabble » et d’obtenir ainsi la prime de 50 points.

"""

    def __init__(self, master):
        super().__init__(master)
        self.title("Règlements de PyScrabble")

        frame = Frame(self)
        frame.pack()

        text = Text(frame, width=120)
        text.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)

        scroll = Scrollbar(frame, command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)

        text.config(yscrollcommand=scroll.set)

        text.tag_configure("h1", font="Times 14 bold")
        text.tag_configure("h2", font="Times 12 bold")

        text.insert(END, "Règlements de PyScrabble\n\n", "h1")
        text.insert(END, "Généralités", "h2")
        text.insert(END, Reglements.GENERALITES)
        text.insert(END, "Début de la partie", "h2")
        text.insert(END, Reglements.DEBUT)
        text.insert(END, "Déroulement de la partie", "h2")
        text.insert(END, Reglements.DEROULEMENT)
        text.insert(END, "Décompte des points", "h2")
        text.insert(END, Reglements.DECOMPTE)

        text.config(state="disabled")


if __name__ == "__main__":

    Reglements(Tk()).mainloop()
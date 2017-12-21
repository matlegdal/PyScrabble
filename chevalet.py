from joueur import Joueur
from utils import *
from tkinter import Canvas


class Chevalet(Canvas):
    """
    Cette classe représente le chevalet actif dans l'interface. Elle hérite de la classe Canvas de tkinter.
    """
    TAILLE_CHEVALET = 7
    # todo: refactorer -> bouger taille_chevalet et pixels par case

    def __init__(self, root, parent, pixels_par_case):
        super().__init__(parent, height=pixels_par_case, width=pixels_par_case*Chevalet.TAILLE_CHEVALET, bg='#f5ebdc')
        self.pixels_par_case = pixels_par_case
        self.root = root
        self.bind('<Configure>', self.redimensionner_chevalet)


    def dessiner(self, joueur):
        """
        Cette fonction dessine le chevalet du joueur actif dans le chevalet actif.
        :param joueur: (obj Joueur) Joueur actif
        :return: Aucun
        """
        assert isinstance(joueur, Joueur)

        for pos in range(self.TAILLE_CHEVALET):
            if joueur.chevalet[pos] is None:
                continue

            x1, y1, x2, y2, delta = coord_pos(pos, self.pixels_par_case)
            dessiner_jeton(self, x1, y1, x2, y2, delta, joueur.chevalet[pos], ('chevalet', 'chevalet{}'.format(pos)))

    def redimensionner_chevalet(self, event):
        """
        Fonction qui calcule la nouvelle dimension des cases et redessine le chevalet lors d'un redimenstionnement de la fenêtre.
        :param event: événement de redimensionnement à l'origine du callback
        """
        new_dim = min(event.width, event.height)
        self.pixels_par_case = new_dim//Chevalet.TAILLE_CHEVALET
        self.delete('chevalet')
        self.dessiner(self.root.joueur_actif) # problème ici

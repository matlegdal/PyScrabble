from joueur import Joueur
from utils import *
from tkinter import Canvas


class Chevalet(Canvas):
    """
    Cette classe représente le chevalet actif dans l'interface. Elle hérite de la classe Canvas de tkinter.
    """
    TAILLE_CHEVALET = 7
    # todo: refactorer -> bouger taille_chevalet et pixels par case

    def __init__(self, master, pixels_par_case):
        super().__init__(master, height=pixels_par_case, width=pixels_par_case*Chevalet.TAILLE_CHEVALET, bg='#f5ebdc')
        self.pixels_par_case = pixels_par_case


    def dessiner(self, chevalet):
        """
        Cette fonction dessine le chevalet du joueur actif dans le chevalet actif.
        :param chevalet: list, Jeton, Une liste des jetons à dessiner. Peut-être le chevalet d'un joueur ou les jetons à jeter.
        :return: Aucun
        """
        self.delete('chevalet')
        assert isinstance(chevalet, list)
        assert all([(isinstance(jeton, Jeton) or jeton is None) for jeton in chevalet])

        for pos in range(self.TAILLE_CHEVALET):
            if chevalet[pos] is None:
                continue

            x1, y1, x2, y2, delta = coord_pos(pos, self.pixels_par_case)
            dessiner_jeton(self, x1, y1, x2, y2, delta, chevalet[pos], ('chevalet', 'chevalet{}'.format(pos)))
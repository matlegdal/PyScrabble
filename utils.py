from tkinter import *
from jeton import Jeton

def coord_pos(pos, pixels_par_case):
    """
    Fonction utilitaire pour donner les coins du rectangle lorsqu'un jeton est dessiné sur le chevalet
    :param pos: int, La position sur le chevalet
    :param pixels_par_case: int, La taille des cases
    :return: tuple, retourne les 4 coordonnées du rectangle et le delta utilisé pour le positionnement du texte.
    """
    x1 = pos * pixels_par_case
    y1 = 0
    x2 = x1 + pixels_par_case
    y2 = y1 + pixels_par_case
    delta = int(pixels_par_case / 2)

    return x1, y1, x2, y2, delta

def coord_case(ligne, col, pixels_par_case):
    """
    Fonction utilitaire pour donner les coins du rectangle à dessiner lorsqu'on dessine un jeton sur le plateau
    :param ligne: int, l'index de la ligne
    :param col: int, l'index de la colonne
    :param pixels_par_case: int, la taille des cases
    :return: tuple, retourne les 4 coordonnées du rectangle et le delta utilisé pour le positionnement du texte.
    """
    x1 = col * pixels_par_case
    y1 = ligne * pixels_par_case
    x2 = x1 + pixels_par_case
    y2 = y1 + pixels_par_case
    delta = int(pixels_par_case / 2)

    return x1, y1, x2, y2, delta

def dessiner_jeton(parent, x1, y1, x2, y2, delta, jeton, tags):
    """
    Fonction qui dessine un jeton sur un canvas étant donné les coordonnées et le jeton fourni
    :param parent: Obj héritant de tk.Canvas, Peut être Plateau ou Chevalet
    :param x1: int, la coordonnée x1 du rectangle
    :param y1: int, la coordonnée y1 du rectangle
    :param x2: int, la coordonnée x2 du rectangle
    :param y2: int, la coordonnée y2 du rectangle
    :param delta: int, utilisé pour le placement du texte
    :param jeton: Jeton, Le jeton à dessiner
    :param tags: tuple ou str, les tags à ajouter au rectangle dessiné. Peut être de type str, s'il y en a juste 1. Si plusieurs, doit être un tuple.
    :return: Rien
    """
    assert isinstance(parent, Canvas)
    assert isinstance(jeton, Jeton)

    parent.create_rectangle(x1, y1, x2, y2, fill="ivory", tags=tags)
    parent.create_text(x1 + delta, y1 + delta, justify=CENTER, text=str(jeton), font=("Times", int(delta)), tags=tags)

def mot_permis(mot, dictionnaire):
    """
    Permet de savoir si un mot est permis dans la partie ou pas en regardant dans le dictionnaire.
    :param mot: str, mot à vérifier.
    :param dictionnaire: set, Dictionnaire des mots.
    :return: bool, True si le mot est dans le dictionnaire, False sinon.
    """
    return mot.upper() in dictionnaire

def bind_poser(master):
    """
    Fonction utilitaire pour binder le clic de souris à la pose d'un jeton sur une case
    """
    master.plateau.tag_bind('case', '<Button-1>', master.poser_jeton)

def unbind_poser(master):
    """
    Fonction utilitaire pour unbinder le clic de souris à la pose d'un jeton sur une case
    """
    master.plateau.tag_bind('case', '<Button-1>', lambda e: "break")

def bind_prendre(master):
    """
    Permet de binder la prise d'un jeton dans le chevalet
    """
    master.chevalet_actif.tag_bind('chevalet', '<Button-1>', master.prendre_jeton)

def unbind_prendre(master):
    """
    Permet de unbinder la prise d'un jeton dans le chevalet
    """
    master.chevalet_actif.tag_bind('chevalet', '<Button-1>', lambda e: "break")

def bind_jeter(master):
    master.chevalet_actif.tag_bind('chevalet', '<Button-1>', master.jeter_jeton)

def unbind_jeter(master):
    master.chevalet_actif.tag_bind('chevalet', '<Button-1>', lambda e: "break")

def bind_reprendre(master):
    """
    Fonction utilitaire pour binder le clic de souris aux jetons placés.
    """
    master.plateau.tag_bind('jeton_place', '<Button-1>', master.reprendre_jeton)

def bind_redeposer(master):
    """
    Fonction utilitaire pour binder le clic de souris au chevalet. Utilisé pour éviter que les événements de prendre un jeton
    et de redéposer un jeton ne soient déclenchés par le même clic de souris.
    """
    master.chevalet_actif.bind('<Button-1>', master.redeposer_jeton)

def unbind_redeposer(master):
    """
    Fonction utilitaire pour unbinder le clic de souris au chevalet. Utilisé pour éviter que les événements de prendre un jeton
    et de redéposer un jeton ne soient déclenchés par le même clic de souris.
    """
    master.chevalet_actif.bind('<Button-1>', lambda e: "break")

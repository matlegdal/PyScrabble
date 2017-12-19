from tkinter import *
from jeton import Jeton

def coord_pos(pos, pixels_par_case):
    x1 = pos * pixels_par_case
    y1 = 0
    x2 = x1 + pixels_par_case
    y2 = y1 + pixels_par_case
    delta = int(pixels_par_case / 2)

    return x1, y1, x2, y2, delta

def coord_case(ligne, col, pixels_par_case):
    x1 = col * pixels_par_case
    y1 = ligne * pixels_par_case
    x2 = x1 + pixels_par_case
    y2 = y1 + pixels_par_case
    delta = int(pixels_par_case / 2)

    return x1, y1, x2, y2, delta

def dessiner_jeton(master, x1, y1, x2, y2, delta, jeton, tags):
    assert isinstance(master, Canvas)
    assert isinstance(jeton, Jeton)

    master.create_rectangle(x1, y1, x2, y2, fill="ivory", tags=tags)
    master.create_text(x1 + delta, y1 + delta, justify=CENTER, text=str(jeton), font=("Times", int(delta)), tags=tags)

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
    master.chevalet_actif.tag_bind('chevalet', '<Button-1>', master.prendre_jeton)

def unbind_prendre(master):
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

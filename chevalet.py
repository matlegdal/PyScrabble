from case import Case
from utils import *
from tkinter import Canvas, CENTER, Tk, NSEW
from exception import *


class Chevalet(Canvas):
    """
    Cette classe représente le chevalet du joueur. Elle hérite de la classe Canvas de tkinter.
    """
    TAILLE_CHEVALET = 7

    def __init__(self, master):
        super().__init__(master)
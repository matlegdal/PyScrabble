from tkinter import Canvas, Frame, Tk, Label
from joueur import Joueur

# TODO: faire afficher le chevalet correctement


class Aside(Frame):
    """
    Classe héritant de Frame. Est un cadre qui contient le chevalet du joueur actif et des informations.
    Contient aussi les boutons de jeu.
    :param: La fenêtre dans lequel il s'affichera.
    """
    TAILLE_CHEVALET = 7

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pixel_par_case = 60
        self.aside_frame = Frame(self, width=60*7, height=self.pixel_par_case)

        self.dessiner()
        self.label_joueur_actif = Label(self.aside_frame, text="Joueur {joueur_actif.nom}")
        self.label_joueur_actif.grid(row=0)
        self.bind('<Configure>', self.redimensionner)

    def dessiner(self):
        Chevalet(self.aside_frame).grid(row=1)

    def redimensionner(self, event):
        new_dim = min(event.width, event.height)
        self.pixel_par_case = new_dim//Aside.TAILLE_CHEVALET
        # todo: faire fonctionner le redimensionnement

class Chevalet(Canvas):

    """
    Classe Canvas qui représente le chevalet du joueur actif.
    :param: l'entité dans lequel il sera affiché (objet Aside)

    """
    pixel_par_case = 60
    TAILLE_CHEVALET = 7

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.dessiner_chevalet_joueur_actif()
        self.bind('<Configure>', self.redimensionner)

    def dessiner_chevalet_joueur_actif(self):

        for cases in range(Chevalet.TAILLE_CHEVALET):
            x1 = cases * Chevalet.pixel_par_case
            y1 = Chevalet.pixel_par_case
            x2 = x1 + Chevalet.pixel_par_case
            y2 = 0
            self.create_rectangle(x1, y1, x2, y2, fill="white", tags='cases')

    def redimensionner(self, event):
        new_dim = min(event.width, event.height)
        self.pixel_par_case = new_dim//Chevalet.TAILLE_CHEVALET
        # todo: faire fonctionner le redimensionnement


if __name__ == '__main__':
    fenetre = Tk()
    chevalet = Aside(fenetre)
    fenetre.mainloop()
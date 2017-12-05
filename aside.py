from tkinter import Canvas, Frame, Tk


class Aside(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

    def dessiner(self):
        self.chevalet = Chevalet.dessiner_chevalet_joueur_actif(self)
        self.chevalet.grid(row=1)


class Chevalet(Canvas):
    pixel_par_case = 60
    TAILLE_CHEVALET = 7

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.dessiner_chevalet_joueur_actif()

    def dessiner_chevalet_joueur_actif(self):

        for cases in range(Chevalet.TAILLE_CHEVALET):
            x1 = cases * Chevalet.pixel_par_case
            y1 = x1
            x2 = x1 + Chevalet.pixel_par_case
            y2 = x1
            self.create_rectangle(x1, y1, x2, y2, fill="ivory", tags='cases')


if __name__ == '__main__':
    fenetre = Tk()
    chevalet = Chevalet(fenetre)
    fenetre.mainloop()
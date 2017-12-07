from tkinter import *
from jeton import Jeton
# from tkinter.dnd import dnd_start, DndHandler

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

def dessiner_jeton(master, x1, y1, x2, y2, delta, jeton, tag):
    assert isinstance(master, Canvas)
    assert isinstance(jeton, Jeton)

    master.create_rectangle(x1, y1, x2, y2, fill="ivory", tags=tag)
    master.create_text(x1 + delta, y1 + delta, justify=CENTER, text=str(jeton), font=("Times", int(delta)), tags=tag)

# class DragJeton(Frame):
#     def __init__(self, master, pixels_par_case, jeton, event):
#         super().__init__(master)
#         self.canvas = Canvas(self, width=pixels_par_case, height=pixels_par_case, bg="grey")
#         self.canvas.grid()
#         self.taille = pixels_par_case
#         self.jeton = jeton
#         self.drag_start_x = master.affichage_joueur.winfo_x() + master.chevalet_actif.winfo_x() + event.x
#         self.drag_start_y = master.affichage_joueur.winfo_y() + master.chevalet_actif.winfo_y() + event.y
#
#     def start_drag(self):
#         self.place(x=self.drag_start_x, y=self.drag_start_y)
#         dessiner_jeton(self.canvas, 0, 0, self.taille, self.taille, delta=int(self.taille/2), jeton=self.jeton, tag=None)
#         self.bind('<B1-Motion>', self.on_drag)
#         print("drag start")
#
#     def on_drag(self, event):
#         print('drag motion')
#         x = self.drag_start_x + event.x
#         y = self.drag_start_y + event.y
#         self.place(x=x, y=y)
from tkinter import Canvas, CENTER
from jeton import Jeton

def coord_pos(pos, pixels_par_case):
    assert 0 <= pos <= 6
    assert pixels_par_case == 40

    x1 = pos * pixels_par_case
    y1 = 0
    x2 = x1 + pixels_par_case
    y2 = y1 + pixels_par_case
    delta = int(pixels_par_case / 2)

    return x1, y1, x2, y2, delta

def dessiner_jeton(master, x1, y1, x2, y2, delta, jeton, tag):
    assert isinstance(master, Canvas)
    assert isinstance(jeton, Jeton)

    master.create_rectangle(x1, y1, x2, y2, fill="ivory", tags=tag)
    master.create_text(x1 + delta, y1 + delta, justify=CENTER, text=str(jeton), font=("Times", int(delta)), tags=tag)
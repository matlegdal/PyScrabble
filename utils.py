from tkinter import Canvas, CENTER
from jeton import Jeton

def dessiner_jeton(master, x1, y1, x2, y2, delta, jeton, tag):
    assert isinstance(master, Canvas)
    assert isinstance(jeton, Jeton)

    master.create_rectangle(x1, y1, x2, y2, fill="ivory", tags=tag)
    master.create_text(x1 + delta, y1 + delta, justify=CENTER, text=str(jeton), font=("Times", int(delta)), tags=tag)
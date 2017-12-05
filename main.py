from scrabble import *


#     def jouer(self, nb_joueurs, langue):
#         self.current.destroy()
#
#         self.current = Scrabble(self, nb_joueurs, langue)
#         self.current.grid(rowspan=self.current.plateau.DIMENSION, columnspan=self.current.plateau.DIMENSION+10)
#
#         # Plateau
#         self.current.plateau.grid(row=0, column=0, rowspan=self.current.plateau.DIMENSION, columnspan=self.current.plateau.DIMENSION, sticky=NSEW)
#         self.current.plateau.tag_bind('case', '<Button-1>', self.click_case)
#         # self.bind('<Configure>', self.current.plateau.redimensionner) #TODO: le redimensionage est buggy
#
#         # Joueur
#         # self.current.joueur_suivant()
#
#         Label(self.current, text=self.current.message).grid(row=5, column=15, columnspan=10, sticky=N)
#
#         # TODO: à corriger: fais planter pour l'instant
#         try:
#             self.current.jouer()
#         except:
#             self.current.message = "Oups il y a un problème"
#
#         # self.current.joueur_actif.dessiner_chevalet()
#         # self.current.joueur_actif.grid(row=6, column=15)
#         # self.current.joueur_actif.tag_bind('chevalet', '<Button-1>', self.click_jeton)



Scrabble().mainloop()


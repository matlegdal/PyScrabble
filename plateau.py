from case import Case
from utils import *
from tkinter import Canvas, CENTER, Tk, NSEW
from exception import *


class Plateau(Canvas):
    """
    Cette classe représente un plateau de scrabble. Elle hérite de la classe Canvas de tkinter.
    - DIMENSION qui représente la dimension (nombre de lignes ou de colonnes) pour le plateu de scrabble. Par défaut sa valeur est de 15.

    Un plateau de scrabble a pour attribut:
    - cases: Case list list, une liste de liste de cases.
            Le programmeur peut avoir accès et manipuler les cases du plateau avec des indexes i et j,
            tels que 0 <= i < Plateau.DIMENSION et 0 <= j < Plateau.DIMENSION.
    - positions: tuple list, Liste des positions sous la forme du tuple (i, j) des cases sur lesquels ont été placés des jetons au cours du tour courant.
    - jetons_placés: Jeton list, Liste des jetons placés lors du tour courant
    """
    DIMENSION = 15

    def __init__(self, master, pixels_par_case):
        """Constructeur d'un plateau.
        :param master: Fenêtre principale, de type Tk
        :param pixels_par_case: Taille des cases en pixels
        """
        super().__init__(master, height=pixels_par_case*Plateau.DIMENSION, width=pixels_par_case*Plateau.DIMENSION)
        self.master = master
        self.pixels_par_case = pixels_par_case
        self.positions = []
        self.jetons_places = []
        self.tour = 0

        self.cases = [[Case() for _ in range(Plateau.DIMENSION)] for _ in range(Plateau.DIMENSION)]
        for (i, j) in [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]:
            self.cases[i][j] = Case(3, 'M')
        for (i, j) in [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),
                       (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]:
            self.cases[i][j] = Case(3, 'L')
        for i in [1, 2, 3, 4]:
            self.cases[i][i] = Case(2, 'M')
            self.cases[i][Plateau.DIMENSION - i - 1] = Case(2, 'M')
            self.cases[Plateau.DIMENSION - i - 1][Plateau.DIMENSION - i - 1] = Case(2, 'M')
            self.cases[Plateau.DIMENSION - i - 1][i] = Case(2, 'M')
        for i, j in [(1, 1), (4, 0), (0, 4), (5, 1), (1, 5), (7, 4)]:
            self.cases[7 - i][7 - j] = Case(2, 'L')
            self.cases[7 + i][7 - j] = Case(2, 'L')
            self.cases[7 - i][7 + j] = Case(2, 'L')
            self.cases[7 + i][7 + j] = Case(2, 'L')
        self.cases[7][7] = Case(2, 'M')

        self.dessiner()
        self.bind('<Configure>', self.redimensionner)

    def dessiner(self):
        self.delete('case')
        self.delete('jeton')

        for ligne in range(Plateau.DIMENSION):
            for col in range(Plateau.DIMENSION):
                x1, y1, x2, y2, delta = coord_case(ligne, col, self.pixels_par_case)
                self.create_rectangle(x1, y1, x2, y2, fill=self.cases[ligne][col].code_couleur, tags="case")

                if ligne == col and ligne == 7:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER, text='\u2605', font=("Times", delta), tags='case')

                else:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER,
                                     text="{}".format(self.cases[ligne][col].text_case()),
                                     font=("Times", int(delta/2)), tags='case')
                if not self.cases[ligne][col].est_vide():
                    dessiner_jeton(self, x1, y1, x2, y2, delta, self.cases[ligne][col].jeton_occupant, 'jeton')


    def redimensionner(self, event):
        new_dim = min(event.width, event.height)
        self.pixels_par_case = new_dim//Plateau.DIMENSION
        self.delete('case')
        self.delete('jeton')
        self.dessiner()
        # TODO: corriger le bug avec le redimensionnement lorsqu'on a placé des jetons au cours du tour

    def case_est_vide(self, ligne, col):
        """
        Permet de déterminer si une case est vide, c'est-à-dire qu'elle ne contient pas de jeton.
        :param ligne: int, index de la ligne
        :param col: int, index de la colonne
        :return: True si la case est vide, False sinon. Rappelez-vous qu'il existe une méthode est_vide disponible pour les objets de type Case.
        :exception: Levez une exception avec assert si le code de la position est invalide.
        """
        if 0 > ligne >= self.DIMENSION or 0 > col >= self.DIMENSION:
            raise PositionInvalideException("La position de la case n'est pas valide.")

        return self.cases[ligne][col].est_vide()

    def est_vide(self):
        """
        Permet de déterminer si le plateau est vide, c'est à dire que toutes les cases sont vides.
        :return: True si le plateau est vide, False sinon.
        """
        return all([case.est_vide() for ligne in self.cases for case in ligne])

    def ajouter_jeton(self, jeton, ligne, col):
        """
        Permet d'ajouter un jeton dans une case vide du plateau.
        :param jeton: Jeton, le jeton à ajouter sur le plateau.
        :param ligne: int, index de la ligne
        :param col: int, index de la colonne
        :return: Ne retourne rien.
        :exception: Levez une exception si la case n'est pas vide.
        """
        if not self.case_est_vide(ligne, col):
            raise CaseOccupeeException("La case est déjà occupée")

        self.cases[ligne][col].placer_jeton(jeton)

    def retirer_jeton(self, ligne, col):
        """
        Permet d'enlever le jeton dans une case du plateau.
        :param ligne: int, index de la ligne
        :param col: int, index de la colonne
        :return: Jeton, le jeton à enlever du plateau.
        :exception: Levez une exception si la case est vide
        """
        if self.case_est_vide(ligne, col):
            raise CaseVideException("Erreur: La case est vide.")

        return self.cases[ligne][col].retirer_jeton()

    def cases_adjacentes_occupees(self, position):
        """
        Étant donnée une position, cette méthode permet de voir si au moins l'une de ses positions voisines est occupée.
        Les cases voisines sont les cases juste en haut, en bas, à gauche et à droite de la case concernée.
        NB: Les cases voisines diagonales ne comptent pas.
        :param position: tuple, position sous la forme (ligne, colonne)
        :return: True si au moins l'une des cases voisines est occupée, False si aucune case voisine n'est occupée.
        :exception: Levez une exception avec assert si le code de la position est invalide
        """
        ligne, col = position
        if 0 > ligne >= self.DIMENSION or 0 > col >= self.DIMENSION:
            raise PositionInvalideException("La position de la case n'est pas valide.")

        # On calcule les positions voisines
        voisins = [(ligne, col - 1), (ligne, col + 1), (ligne + 1, col), (ligne - 1, col)]

        # On vérifie que les positions des voisins sont dans les limites du plateau
        voisins = [(i, j) for i, j in voisins if (0 <= i < Plateau.DIMENSION) and (0 <= j < Plateau.DIMENSION)]

        # On enlève les positions qui sont des cases qui ont été joués dans le tour courant
        voisins_a_retirer = []
        for (i,j) in voisins:
            if (i,j) in self.positions:
                voisins_a_retirer.append((i,j))
        for voisin in voisins_a_retirer:
            voisins.remove(voisin)

        au_moins_une_case_adjacente_occupee = any([not self.cases[i][j].est_vide() for (i, j) in voisins])

        return au_moins_une_case_adjacente_occupee

    def valider_positions(self, positions):
        """
        Étant données des positions où un utilisateur veut placer ses jetons, cette méthode permet de valider
        s'il peut réelement ajouter les jetons à ces positions.
        Les positions sont valides si:
         - elles sont toutes vides;
         - elles sont toutes sur la même ligne ou la même colonne;
         - une fois qu'elles seront placées sur une même ligne ou une même colonne, elles formeront un mot et pas plus
            sur cette même ligne ou colonne. Ici, le mot formé n'est pas important du tout donc n'essayez pas de le trouver;
            Par exemple, si toutes les positions sont sur la ligne 5, votre code doit juste s'assurer qu'entre les positions
            où vous devez ajouter des jetons, des cases ne sont vides.
         - si le plateau est vide, le centre du plateau doit être dans les positions;
         - sinon, au moins une des positions doit être adjacente à une des cases occupées
         du plateau (Pensez à réutilisez cases_adjacentes_occupees et case_est_vide).
        :param positions: list, Liste des positions sous forme de tuples (ligne, col)
        :return: True si les positions sont valides, rien sinon
        :exception: Des exceptions sont levés pour chaque type d'erreur
        """
        positions_cp = self.positions

        # On mappe les positions en lignes et colonnes
        lignes, cols = zip(*positions)
        lignes, cols = list(set(lignes)), list(set(cols))

        # On vérifie que les cases utilisées sont en ligne
        meme_ligne, meme_col = len(lignes) == 1, len(cols) == 1
        if not meme_ligne and not meme_col:
            raise CasesNonEnLigneException('Les cases ne sont pas en ligne')

        # On vérifie que les cases utilisées touchent à au moins une case occupée du plateau (ou le centre si c'est le 1er tour)
        if self.tour == 1:
            if (7, 7) not in positions:
                raise CentreNonUtilise("Le centre doit être utilisé lors du premier tour")
        else:
            au_moins_une_case_adjacente_occupee = any([self.cases_adjacentes_occupees(pos) for pos in positions])
            if not au_moins_une_case_adjacente_occupee:
                raise PasDeCasesAdjacentes("Au moins un des jetons placés doit être adjacent à un jeton du plateau.")

        # On vérifie qu'il n'y a pas de 'trous' dans les mots placés
        if meme_ligne:
            ligne, n, m = lignes[0], min(cols), max(cols)
            if any([(not self.cases[ligne][i].est_vide()) for i in range(n, m + 1) if i not in cols]):
                raise CaseVideDansMot("Il ne doit pas y avoir de cases vides entre les lettres placées")
                #todo: corriger le bug -> ne fonctionne pas comme il devrait
        elif meme_col:
            col, n, m = cols[0], min(lignes), max(lignes)
            if any([(not self.cases[i][col].est_vide()) for i in range(n, m + 1) if i not in lignes]):
                raise CaseVideDansMot("Il ne doit pas y avoir de cases vides entre les lettres placées")

        assert positions_cp == self.positions == positions
        return

    def mots_score_obtenus(self, positions):
        """
        Trouver les mots ajoutés et le score total obtenu lorsque le joueur vient juste d'ajouter des jetons aux positions de la liste en argument.
        :param positions: str list, liste de tuples des positions sous forme (ligne, col)
        :return: (tuple): L'ensemble des mots formés par l'ajout de jetons aux nouvelles positions et le score obtenu
        """
        score_total = 0
        lignes, cols = zip(*positions)
        mots = []
        for ligne in set(lignes):
            lmots, score = self.__mots_et_score_sur_ligne_ou_colonne(positions, ligne)
            mots += lmots
            score_total += score
        for col in set(cols):
            lmots, score = self.__mots_et_score_sur_ligne_ou_colonne(positions, colonne=col)
            mots += lmots
            score_total += score
        return mots, score_total

    def __mots_et_score_sur_ligne_ou_colonne(self, positions, ligne=None, colonne=None):
        """
        Permet de trouver les mots sur une ligne ou une colonne et le score associé.
        :param positions: str list, liste de tuples des positions sous forme (ligne, col)
        :param ligne: (int, optionel), index de la ligne d'intérêt
        :param colonne: (int, optionel), index de la colonne d'intérêt
        :return: tuple (str list, int), la liste des mots trouvés sur la ligne ou la colonne et le score total.
        Plus précisément la liste devra contenir au maximum un élément car un tout nouvel ajout de jetons ne peut pas
        créer plus d'un mot sur la même ligne ou colonne.
        :exception: Levez une exception avec assert si la ligne et la colonne sont spécifiées ou aucun des deux ne l'est.
        """
        assert (ligne is None) ^ (colonne is None), "Précisez seulement la ligne ou la colonne, pas les deux."

        mots, score_total = [], 0
        mot, score_mot, multiplicateur, pos_mot = "", 0, 1, []
        for i in range(Plateau.DIMENSION):
            pos = (ligne, i) if ligne is not None else (i, colonne)
            case = self.cases[pos[0]][pos[1]]
            if case.est_vide():
                if len(mot) > 1 and any([p in pos_mot for p in positions]):
                    mots.append(mot)
                    score_total += score_mot * multiplicateur
                mot, score_mot, multiplicateur, pos_mot = "", 0, 1, []
            else:
                mot += case.lettre_jeton()
                pos_mot.append(pos)
                if pos in positions and case.type == "L":
                    score_mot += case.valeur_jeton() * case.multiplicateur
                else:
                    score_mot += case.valeur_jeton()
                if pos in positions and case.type == "M":
                    multiplicateur *= case.multiplicateur
        if len(mot) > 1 and any([p in pos_mot for p in positions]):
            mots.append(mot)
            score_total += score_mot * multiplicateur

        return mots, score_total



# Tests unitaires

if __name__ == '__main__':
    master = Tk()
    plateau = Plateau(master, 60)
    plateau.grid(row=0, column=0, sticky=NSEW)
    master.mainloop()

    """
    from jeton import Jeton
    # init de quelques jetons
    jetonA = Jeton('A', 1)
    jetonB = Jeton('B', 3)
    jetonC = Jeton('C', 3)
    jetonD = Jeton('D', 2)
    jetonR = Jeton('R', 1)

    # Plateau nouvellement initié est vide
    plateau = Plateau()
    assert plateau.est_vide()

    # l'ajout d'un jeton se passe bien
    plateau.ajouter_jeton(jetonA, 'a1')
    assert not plateau.est_vide()
    assert not plateau.case_est_vide('a1')

    # la suppression d'un jeton
    plateau.retirer_jeton('a1')
    assert plateau.est_vide()
    assert plateau.case_est_vide('a1')

    # l'ajout des jetons dans places_mots se passe bien.
    ret_mot = plateau.placer_mots([jetonC, jetonA, jetonR], ['h8', 'h9', 'h10'])
    assert not plateau.case_est_vide('h8') and not plateau.case_est_vide('h9') and not plateau.case_est_vide('h10')
    assert plateau.cases[Plateau.decode_position('h8')[0]][Plateau.decode_position('h8')[1]].jeton_occupant == jetonC
    assert plateau.cases[Plateau.decode_position('h9')[0]][Plateau.decode_position('h9')[1]].jeton_occupant == jetonA
    assert plateau.cases[Plateau.decode_position('h10')[0]][Plateau.decode_position('h10')[1]].jeton_occupant == jetonR

    # le return de placer_mots est le bon
    assert ret_mot == (['CAR'], 10), "Le return de placer_mot ne concorde pas"
    """


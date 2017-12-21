from case import Case
from utils import *
from tkinter import Canvas, CENTER
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

    def __init__(self, root, parent, pixels_par_case, cases=None):
        """Constructeur d'un plateau.
        :param root: Fenêtre principale, de type Tk. Correspond à l'objet Scrabble.
        :param parent: Frame, dans lequel se trouve le plateau. Correspond à Scrabble.content.
        :param pixels_par_case: Taille des cases en pixels
        :param cases: list, list, cases, Liste des cases du plateau. None par défaut, passé en argument si on charge une partie.
        """
        super().__init__(parent, height=pixels_par_case*Plateau.DIMENSION, width=pixels_par_case*Plateau.DIMENSION)
        self.root = root
        self.pixels_par_case = pixels_par_case

        self.positions = []
        self.jetons_places = []

        if cases is None:
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
        else:
            self.cases = list(cases)

        self.dessiner()
        self.bind('<Configure>', self.redimensionner)

    def dessiner(self):
        """
        Dessine les cases et les jetons sur le canevas du plateau.
        """
        self.delete('case')
        self.delete('jeton')

        for ligne in range(Plateau.DIMENSION):
            for col in range(Plateau.DIMENSION):
                # Dessin des cases
                x1, y1, x2, y2, delta = coord_case(ligne, col, self.pixels_par_case)
                self.create_rectangle(x1, y1, x2, y2, fill=self.cases[ligne][col].code_couleur, tags="case")

                # Cases spéciales
                if ligne == col and ligne == 7:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER, text='\u2605', font=("Times", delta), tags='case')
                else:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER,
                                     text="{}".format(self.cases[ligne][col].text_case()),
                                     font=("Times", int(delta/2)), tags='case')

                # Dessin des jetons
                if not self.cases[ligne][col].est_vide():
                    tags=['jeton']
                    if self.cases[ligne][col].jeton_occupant in self.jetons_places:
                        tags.append('jeton_place')
                        tags.append('jeton_{}_{}'.format(ligne, col))

                    dessiner_jeton(self, x1, y1, x2, y2, delta, self.cases[ligne][col].jeton_occupant, tags=tuple(tags))

    def redimensionner(self, event):
        """
        Fonction qui calcule la nouvelle dimension des cases et redessine le plateau lors d'un redimenstionnement de la fenêtre.
        :param event: événement de redimensionnement à l'origine du callback
        """
        new_dim = min(event.width, event.height)
        self.pixels_par_case = new_dim//Plateau.DIMENSION
        self.delete('case')
        self.delete('jeton')
        self.dessiner()

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

    def etait_vide(self):
        """
        Permet de déterminer si le plateau était vide avant le tour courant, c'est à dire que toutes les cases étaient vides.
        :return: True si le plateau était vide, False sinon.
        """
        # On enlève de la liste des cases à vérifier les positions occupées lors du tour courant
        cases_a_verifier = [self.cases[ligne][col] for ligne in range(Plateau.DIMENSION) for col in range(Plateau.DIMENSION) if (ligne, col) not in self.positions]
        # On vérifie si toutes les cases à vérifier sont vides
        etait_vide = all([case.est_vide() for case in cases_a_verifier])
        return etait_vide

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
        NB: Les cases voisines diagonales ne comptent pas et les cases jouées lors du tour courant (représenté par Plateau.positions) ne comptent pas non plus
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
        voisins_a_retirer = [(i,j) for (i,j) in voisins if (i,j) in self.positions]
        for voisin in voisins_a_retirer:
            voisins.remove(voisin)

        au_moins_une_case_adjacente_occupee = any([not self.cases[i][j].est_vide() for (i, j) in voisins])

        return au_moins_une_case_adjacente_occupee

    def valider_positions(self, positions):
        """
        Étant données des positions où un utilisateur veut placer ses jetons, cette méthode permet de valider
        s'il peut réelement ajouter les jetons à ces positions.
        Les positions sont valides si:
         - elles sont toutes sur la même ligne ou la même colonne;
         - une fois qu'elles sont placées sur une même ligne ou une même colonne, il n'y a pas de cases vides entre les cases occupées
         - si le plateau est vide, le centre du plateau doit être dans les positions;
         - sinon, au moins une des positions doit être adjacente à une des cases occupées du plateau
        :param positions: list, Liste des positions sous forme de tuples (ligne, col)
        :return: True si les positions sont valides, rien sinon
        :exception: Des exceptions sont levés pour chaque type d'erreur
        """
        # On mappe les positions en lignes et colonnes
        lignes, cols = zip(*positions)
        lignes, cols = list(set(lignes)), list(set(cols))

        # On vérifie que les cases utilisées sont en ligne
        meme_ligne, meme_col = len(lignes) == 1, len(cols) == 1
        if not meme_ligne and not meme_col:
            raise CasesNonEnLigneException('Les cases ne sont pas en ligne')

        # On vérifie que les cases utilisées touchent à au moins une case occupée du plateau (ou le centre si c'est le 1er tour)
        if self.etait_vide():
            if (7, 7) not in positions:
                raise CentreNonUtilise("Le centre doit être utilisé lors du premier tour")
        else:
            au_moins_une_case_adjacente_occupee = any([self.cases_adjacentes_occupees(pos) for pos in positions])
            if not au_moins_une_case_adjacente_occupee:
                raise PasDeCasesAdjacentes("Au moins un des jetons placés doit être adjacent à un jeton du plateau.")

        # On vérifie qu'il n'y a pas de 'trous' dans les mots placés
        if meme_ligne:
            ligne, n, m = lignes[0], min(cols), max(cols)
            au_moins_un_trou = any([self.cases[ligne][col].est_vide() for col in range(n, m + 1) if col not in cols])
            if au_moins_un_trou:
                raise CaseVideDansMot("Il ne doit pas y avoir de cases vides entre les lettres placées")
        elif meme_col:
            col, n, m = cols[0], min(lignes), max(lignes)
            au_moins_un_trou = any([self.cases[ligne][col].est_vide() for ligne in range(n, m + 1) if ligne not in lignes])
            if au_moins_un_trou:
                raise CaseVideDansMot("Il ne doit pas y avoir de cases vides entre les lettres placées")

        return True

    def mots_score_obtenus(self, positions):
        """
        Trouver les mots ajoutés et le score total obtenu lorsque le joueur vient juste d'ajouter des jetons aux positions de la liste en argument.
        :param positions: str list, liste de tuples des positions sous forme (ligne, col)
        :return: (tuple): L'ensemble des mots formés par l'ajout jetons aux nouvelles positions et le score obtenu
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
        if (ligne is None) ^ (colonne is None) is False:
            raise LigneColonneSpecifiee("Précisez seulement la ligne ou la colonne, pas les deux.")

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



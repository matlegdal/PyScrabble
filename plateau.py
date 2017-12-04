from case import Case
from tkinter import Canvas, CENTER, Tk, NSEW
from exception import *


class Plateau(Canvas):
    """
    Cette classe représente un plateau de scrabble.
    Une partie de la logique du jeu sera implémentée ici donc lisez bien les spécifications de chaque méthode.
    ex:
             1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        A |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | A
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        B |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | B
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        C |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | C
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        D |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | D
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        E |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | E
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        F |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | F
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        G |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | G
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        H |    |    |    |    |    |    |    | ★  |    |    |    |    |    |    |    | H
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        I |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | I
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        J |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | J
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        K |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | K
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        L |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | L
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        M |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | M
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        N |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | N
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        O |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | O
          +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
             1    2    3    4    5    6    7    8    9   10   11   12   13   14   15

    Nous avons un attribut de classe:
    - DIMENSION qui représente la dimension (nombre de lignes ou de colonnes) pour le plateu de scrabble. Par défaut sa valeur est de 15.

    Un plateau de scrabble a pour attribut:
    - cases: Case list list, une liste de liste de cases.
            Le programmeur peut avoir accès et manipuler les cases du plateau avec des indexes i et j,
            tels que 0 <= i < Plateau.DIMENSION et 0 <= j < Plateau.DIMENSION.
            Pour vous aider un peu:
                * cases[i] vous retourne la i+1 ème ligne du plateau. (L'index i == 0 correspond donc à la première ligne, et ainsi de suite).
                * cases[i][j] vous donne la case au croisement de la i+1 ème ligne et de la j+1 ème colonne du plateau.
                (L'index j == 0 correspond donc à la première colonne, et ainsi de suite).

            L'utilisateur de la classe, désignera les cases grâce à un code au format « XY » où X représente une lettre
            comprise entre 'A' et 'O', et Y un nombre compris entre 1 et 15. Ex: K9, E15.
            - La lettre désigne une ligne: 'A' pour la 1ère ligne, B pour la seconde ligne, etc.
            - Le nombre désigne une colonne: 5 correspond à la 5ème colonne.
            Par exemple:
            - K9 permet de désigner la case à l'intersection de la 11ème ligne et de la 9ème colonne.
            - E15 permet de désigner la case à l'intersection de la 5ème ligne et 15ème colonne.
            Note: Vous pouvez vour servir du graphe ASCII plus haut pour une meilleure compréhension.
    """
    DIMENSION = 15

    def __init__(self, master, pixels_par_case):
        """Constructeur d'un plateau.
        :param master:
        """
        super().__init__(master, height=pixels_par_case*Plateau.DIMENSION, width=pixels_par_case*Plateau.DIMENSION)
        self.master = master
        self.pixels_par_case = pixels_par_case

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
        self.delete('lettre')
        for colonne in range(Plateau.DIMENSION):
            for ligne in range(Plateau.DIMENSION):
                x1 = colonne*self.pixels_par_case
                y1 = ligne*self.pixels_par_case
                x2 = x1 + self.pixels_par_case
                y2 = y1 + self.pixels_par_case

                self.create_rectangle(x1, y1, x2, y2, fill=self.cases[colonne][ligne].code_couleur,
                                      tags="case")
                delta = int(self.pixels_par_case/2)

                if colonne == ligne and colonne == 7:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER, text='\u2605',
                                     font=("Times", delta), tags='case')

                else:
                    self.create_text((x1 + delta, y1 + delta), justify=CENTER,
                                     text="{}".format(self.cases[colonne][ligne]),
                                     font=("Times", int(delta/2)), tags='case')

    def redimensionner(self, event):
        new_dim = min(event.width, event.height)
        self.pixels_par_case = new_dim//Plateau.DIMENSION
        self.delete('case')
        self.delete('lettre')
        self.dessiner()

    @staticmethod
    def code_position_est_valide(code):
        """
        Méthode statique permettant de valider si un code de positionnement sur le tableau est valide ou pas.
        :param code: str au format « XY » ou « xy » représentant un code de positionnement.
        :return: True si le code passé en argument est un code de positionnement au format « XY » ou « xy » valide.
                En gros, c'est insensible à la casse.
        """
        code = code.upper()
        valide = 2 <= len(code) <= 3 and code[0].isalpha() and code[1:].isdigit()
        if valide:
            index_ligne = ord(code[0]) - ord('A')
            index_colonne = int(code[1:]) - 1
            return 0 <= index_ligne < Plateau.DIMENSION and 0 <= index_colonne < Plateau.DIMENSION
        return False

    @staticmethod
    def decode_position(code):
        """
        Méthode statique servant à transformer un code de positionnement sur le plateau
        en index d'accès de ligne et de colonne sur le plateau.

        :param code: str au format « XY » ou « xy » représentant un code de positionnement.

        :return: tuple (int, int), l'index de la ligne et l'index de la colonne associés au code.
        :exception: Levez une exception avec assert si le code de la position est invalide. Pensez à utiliser Plateau.code_position_est_valide.
        """
        if not Plateau.code_position_est_valide(code):
            raise PositionInvalideException("La position de la case n'est pas valide.")

        # Le premier charactère est converti en ordinal et sa position par rapport à 'A' est trouvée. Il s'agit de l'index de la ligne.
        # Les autres caractères sont convertis en integer et on soustrait 1 pour avoir l'index de la colonne.
        return ord(code.upper()[0]) - ord('A'), int(code[1:]) - 1

    def case_est_vide(self, position_code):
        """
        Permet de déterminer si une case est vide, c'est-à-dire qu'elle ne contient pas de jeton.
        :param position_code: str, au format « XY » ou « xy » qui un code de positionnement de la case sur le plateau.
                            Pensez à réutiliser Plateau.decode_position sur position_code.
        :return: True si la case est vide, False sinon. Rappelez-vous qu'il existe une méthode est_vide disponible pour les objets de type Case.
        :exception: Levez une exception avec assert si le code de la position est invalide.
        """
        if not Plateau.code_position_est_valide(position_code):
            raise PositionInvalideException("La position de la case n'est pas valide.")

        ligne, col = Plateau.decode_position(position_code)
        return self.cases[ligne][col].est_vide()

    def est_vide(self):
        """
        Permet de déterminer si le plateau est vide, c'est à dire que toutes les cases sont vides.
        :return: True si le plateau est vide, False sinon.
        """
        return all([case.est_vide() for ligne in self.cases for case in ligne])

    def ajouter_jeton(self, jeton, position_code):
        """
        Permet d'ajouter un jeton dans une case vide du plateau. La case est indiquée grâce à son code de positionnement.
        :param jeton: Jeton, le jeton à ajouter sur le plateau.
        :param position_code: str, la position où ajouter (au format « XY » ou « xy »)
        :return: Ne retourne rien.
        :exception: Levez une exception avec assert si le code de la position est invalide ou la case n'est pas vide.
        """
        if not self.case_est_vide(position_code):
            raise CaseOccupeeException("La case est déjà occupée")

        ligne, col = Plateau.decode_position(position_code)
        self.cases[ligne][col].placer_jeton(jeton)

    def retirer_jeton(self, position_code):
        """
        Permet d'enlever le jeton dans une case du plateau. La case est indiquée grâce à son code de positionnement.
        :param position_code: str, la position où enlever le jeton (au format « XY » ou « xy »).
        :return: Jeton, le jeton à enlever du plateau. Rappelez-vous qu'il existe une méthode retirer_jeton disponible pour les objets de type Case.
        :exception: Levez une exception avec assert si le code de la position est invalide ou la case n'est pas vide. -> erreur si la case EST vide!
        """
        if self.case_est_vide(position_code):
            raise CaseVideException("Erreur: La case est vide.")

        ligne, col = Plateau.decode_position(position_code)
        return self.cases[ligne][col].retirer_jeton()

    def cases_adjacentes_occupees(self, position_code):
        """ *** Vous n'avez pas à coder cette méthode ***
        Étant donnée une position, cette méthode permet de voir si au moins l'une de ses positions voisines est occupée.
        Les cases voisines sont les cases juste en haut, en bas, à gauche et à droite de la case concernée.
        NB: Les cases voisines diagonales ne comptent pas.
        :param position_code: str, la position d'intérêt.
        :return: True si au moins l'une des cases voisines est occupée, False si aucune case voisine n'est occupée.
        :exception: Levez une exception avec assert si le code de la position est invalide
        """

        if not Plateau.code_position_est_valide(position_code):
            raise PositionInvalideException("La position de la case n'est pas valide.")

        index_ligne, index_colonne = Plateau.decode_position(position_code)
        voisins = [(index_ligne, index_colonne - 1), (index_ligne, index_colonne + 1), (index_ligne + 1, index_colonne), (index_ligne - 1, index_colonne)]
        voisins = [(i, j) for i, j in voisins if (0 <= i < Plateau.DIMENSION)
                   and (0 <= j < Plateau.DIMENSION)]
        return any([not self.cases[i][j].est_vide() for (i, j) in voisins])

    def valider_positions_avant_ajout(self, positions_codes):
        """ *** Vous n'avez pas à coder cette méthode ***
        Cette méthode implémente certaines règles du jeu donc soyez attentifs au texte ci-dessous.
        Étant données des positions_codes où un utilisateur veut placer ses jetons, cette méthode permet de valider
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
        :param positions_codes: str list, liste de string représentant les positions où on veut ajouter des jetons.
        :return: True si les positions sont valides, False sinon.
        :exception: Levez une exception avec assert si le code d'une des positions est invalide.
        """
        # Cette méthode gagnerait à être refactorée en utilisant des raise exception pour spécifier des messages d'erreurs beaucoup
        # informatifs afin que le joueur sache pourquoi son input a été refusé.
        positions_decodees = [Plateau.decode_position(p) for p in positions_codes]
        lignes, cols = zip(*positions_decodees)
        lignes, cols = list(set(lignes)), list(set(cols))
        meme_ligne, meme_col = len(lignes) == 1, len(cols) == 1
        valide = meme_ligne or meme_col
        valide = valide and all([self.case_est_vide(p) for p in positions_codes])
        if valide:
            if self.est_vide():
                valide = (7, 7) in positions_decodees
            else:
                valide = any([self.cases_adjacentes_occupees(pos) for pos in positions_codes])

            if valide and meme_ligne:
                ligne, n, m = lignes[0], min(cols), max(cols)
                valide = all([(not self.cases[ligne][i].est_vide()) for i in range(n, m + 1) if i not in cols])
            elif valide and meme_col:
                col, n, m = cols[0], min(lignes), max(lignes)
                valide = all([(not self.cases[i][col].est_vide()) for i in range(n, m + 1) if i not in lignes])

        return valide

    def placer_mots(self, jetons_a_ajouter, position_codes):
        """
        Permet de placer plusieurs jetons sur le plateau afin de former un ou plusieurs mots.
        Pensez à réutiliser valider_positions_avant_ajout.
        :param jetons_a_ajouter: Jetons à ajouter pour placer nos mots. -> liste objets Jetons
        :param position_codes: str list, liste de chaînes de caractères représentant les positions où on veut placer les jetons.
        :return: tuple de type (str list, int):
            - Le premier élement est la liste des mots formés avec les jetons si l'ajout a été fait, liste vide sinon.
            - Le second élément est le score obtenu si l'ajout a été fait, 0 sinon.
        :exception: Levez une exception avec assert si les positions sont invalides.
        """
        if not self.valider_positions_avant_ajout(position_codes):
            raise PositionInvalideException("Les positions ne sont pas valides")

        # On ajoute les jetons aux positions spécifiées
        for jeton, pos in zip(jetons_a_ajouter, position_codes):
            self.ajouter_jeton(jeton, pos)

        # En retour on appelle la fonction mots_score_obtenus() qui nous retourne un tuple: (mots, score)
        return self.mots_score_obtenus(position_codes)

    def mots_score_obtenus(self, nouvelles_positions):
        """ *** Vous n'avez pas à coder cette méthode ***
        Trouver les mots ajoutés et le score total obtenu lorsque le joueur vient juste d'ajouter des jetons aux positions de la liste en argument.
        :param nouvelles_positions: str list, liste de chaînes de caractères représentant les dernières positions où des jetons ont été ajoutés.
        :return: L'ensemble des mots formés par l'ajout de jetons aux nouvelles positions.
        """
        positions_decodees = [Plateau.decode_position(p) for p in nouvelles_positions]
        score_total = 0
        lignes, cols = zip(*positions_decodees)
        mots = []
        for ligne in set(lignes):
            lmots, score = self.__mots_et_score_sur_ligne_ou_colonne(nouvelles_positions, ligne)
            mots += lmots
            score_total += score
        for col in set(cols):
            lmots, score = self.__mots_et_score_sur_ligne_ou_colonne(nouvelles_positions, colonne=col)
            mots += lmots
            score_total += score
        return mots, score_total

    def __mots_et_score_sur_ligne_ou_colonne(self, nouvelles_positions, ligne=None, colonne=None):
        """ *** Vous n'avez pas à coder cette méthode ***
        Permet de trouver les mots sur une ligne ou une colonne et le score associé.
        :param nouvelles_positions:  str list, liste de chaînes de caractères représentant les dernières positions où des jetons ont été ajoutés.
        :param ligne: (int, optionel), index de la ligne d'intérêt
        :param colonne: (int, optionel), index de la colonne d'intérêt
        :return: tuple (str list, int), la liste des mots trouvés sur la ligne ou la colonne et le score total.
        Plus précisément la liste devra contenir au maximum un élément car un tout nouvel ajout de jetons ne peut pas
        créer plus d'un mot sur la même ligne ou colonne.
        :exception: Levez une exception avec assert si la ligne et la colonne sont spécifiées ou aucun des deux ne l'est.
        """
        assert (ligne is None) ^ (colonne is None), "Précisez seulement la ligne ou la colonne, pas les deux."

        positions_decodees = [Plateau.decode_position(p) for p in nouvelles_positions]
        mots, score_total = [], 0
        mot, score_mot, multiplicateur, pos_mot = "", 0, 1, []
        for i in range(Plateau.DIMENSION):
            pos = (ligne, i) if ligne is not None else (i, colonne)
            case = self.cases[pos[0]][pos[1]]
            if case.est_vide():
                if len(mot) > 1 and any([p in pos_mot for p in positions_decodees]):
                    mots.append(mot)
                    score_total += score_mot * multiplicateur
                mot, score_mot, multiplicateur, pos_mot = "", 0, 1, []
            else:
                mot += case.lettre_jeton()
                pos_mot.append(pos)
                if pos in positions_decodees and case.type == "L":
                    score_mot += case.valeur_jeton() * case.multiplicateur
                else:
                    score_mot += case.valeur_jeton()
                if pos in positions_decodees and case.type == "M":
                    multiplicateur *= case.multiplicateur
        if len(mot) > 1 and any([p in pos_mot for p in positions_decodees]):
            mots.append(mot)
            score_total += score_mot * multiplicateur

        return mots, score_total

    def __str__(self):
        """ *** Vous n'avez pas à coder cette méthode ***
         Formatage du plateau pour l'affichage.
         Utilise des codes Unicode, ce qui pourrait causer des problèmes avec le système d'exploitation utilisé par certains.
         :return: str, correspondant au formatage du plateau.
        """
        ligne_separation = '  +' + '----+' * Plateau.DIMENSION + '\n'
        chaine = '   '
        for colonne in range(Plateau.DIMENSION):
            chaine += "{:^5d}".format(colonne+1)
        chaine += '\n'
        chaine += ligne_separation
        for rangee in range(Plateau.DIMENSION):
            chaine += '{} |'.format(chr(ord('A')+rangee))
            for colonne in range(Plateau.DIMENSION):
                if rangee == colonne and rangee == 7 and self.cases[rangee][colonne].est_vide():
                    s = "\x1b[0;30;{}m{:^4s}\x1b[0m".format(self.cases[rangee][colonne].code_couleur, '\u2605')
                else:
                    s = "{:^4s}".format(str(self.cases[rangee][colonne]))
                chaine += s + '|'
            chaine += ' {}\n'.format(chr(ord('A') + rangee))
            chaine += ligne_separation
        chaine += '   '
        for colonne in range(Plateau.DIMENSION):
            chaine += "{:^5d}".format(colonne+1)
        chaine += '\n'
        return chaine


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


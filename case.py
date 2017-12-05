from exception import *


class Case:
    """
    Cette classe représente une case sur un tableau de scrabble.

    Les attributs d'une case sont:
    - multiplicateur: int, >= 1 et <= 3.
                        Si la case n'est pas spéciale son multiplicateur de points est de 1.
                        Autrement, il sera de 2 dans le cas d'une case compte double ou
                        3 dans le cas d'une case compte triple.
    - type: str, 'M' si la case est spéciale et affecte le pointage des mots;
                 'L' si la case est spéciale et affecte le pointage des lettres;
                 None si la case n'est pas spéciale.
    - jeton_occupant: Jeton,
    """

    def __init__(self, multiplicateur=1, type=None):
        """
        Constructeur de la classe.
        Notez qu'une case nouvellement créée est vide, c'est-à-dire le jeton occupant est None.
        :param multiplicateur: (int, optionel) multiplicateur de la case.
        :param type: (str, optionel) type de la case.
        :exception: Levez une exception avec assert si le multiplicateur ne respecte pas
        la condition suivante 1 <= multiplicateur <= 3 ou si le type n'est ni None, ni 'M', ni 'L'.
        """
        if not 1 <= multiplicateur <= 3:
            raise CaseMultiException("Le multiplicateur de la case est inférieur à 1 ou supérieur à 3")

        if type not in [None, 'M', 'L']:
            raise CaseTypeException("La case est d'un type différent de None, 'M' ou 'L'")

        self.multiplicateur = multiplicateur
        self.type = type
        self.jeton_occupant = None


    def est_vide(self):
        """
        Vérifie si une case est vide ou pas (jeton_occupant est None ou pas).
        :return: True si la case est vide, False sinon.
        """
        return self.jeton_occupant is None

    def placer_jeton(self, jeton):
        """
        Place un jeton dans la case.
        :param jeton: Jeton, objet à placer dans la case.
        :return: Ne retourne rien.
        :exception: Levez une exception avec assert si la case est déjà occupée.
        """
        if not self.est_vide():
            raise CaseOccupeeException("La case est déjà occupée.")
        self.jeton_occupant = jeton

    def retirer_jeton(self):
        """
        Retire le jeton de la case.
        :return: Le jeton retiré.
        :exception: Levez une exception avec assert si la case est vide.
        """
        if self.est_vide():
            raise CaseVideException("La case est déjà vide")

        jeton_retire = self.jeton_occupant
        self.jeton_occupant = None

        return jeton_retire

    def valeur_jeton(self):
        """
        Permet de trouver la valeur du jeton dans la case.
        :return: int, valeur du jeton occupant.
        :exception: Levez une exception avec assert si la case est vide.
        """
        if self.est_vide():
            raise CaseVideException("La case est vide")

        return self.jeton_occupant.valeur

    def lettre_jeton(self):
        """
        Permet de trouver la lettre inscrite sur le jeton dans la case.
        :return: str, lettre du jeton occupant.
        :exception: Levez une exception avec assert si la case est vide.
        """
        if self.est_vide():
            raise CaseVideException("La case est vide")
        return self.jeton_occupant.lettre

    @property
    def code_couleur(self):
        """  *** Vous n'avez pas à coder cette méthode ***
        Méthode permettant de trouver la couleur associée à une case.
        :return: int, code de couleur de la case.
        """
        if self.type == "M" and self.multiplicateur == 2:
            return '#ffaccb'
        elif self.type == "M" and self.multiplicateur == 3:
            return '#ff0000'
        elif self.type == "L" and self.multiplicateur == 2:
            return '#00c9ff'
        elif self.type == "L" and self.multiplicateur == 3:
            return '#0051ff'
        else:
            return '#f5ebdc'

    def text_case(self):
        """
        Méthode permettant de trouver le texte associé à une case donnée.
        :return: str, chaine de caractère
        """
        if self.type == 'M' and self.multiplicateur == 2:
            return 'Mot\nDouble'

        elif self.type == 'M' and self.multiplicateur == 3:
            return 'Mot\nTriple'

        elif self.type == 'L' and self.multiplicateur == 2:
            return 'Lettre\nDouble'

        elif self.type == 'L' and self.multiplicateur == 3:
            return 'Lettre\nTriple'

        else:
            return ''

    # def __str__(self):
    #     """
    #     Formatage d'une case. Cette méthode est appelée lorsque vous faites str(v) où v est un case
    #     :return: str, correspondant au formatage de la case.
    #     """
    #     #s = "" if self.est_vide() else str(self.jeton_occupant)
    #     #return "\x1b[0;30;{}m{:^4s}\x1b[0m".format(self.code_couleur, s)
    #
    #     # changement de code pour quelque chose de plus simple et compatible avec le canvas
    #     return Case.text_case(self)

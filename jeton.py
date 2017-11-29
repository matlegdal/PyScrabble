class Jeton:
    """
    Cette classe représente un jeton.

    Les attributs d'un jeton sont:
    - lettre: str, représentant la lettre écrite sur le jeton. Par convention toutes les lettres au scrabble sont en majuscules.
                Dans ce travail nous ne considérons pas les jetons jokers qui n'ont aucune lettre inscrite.
    - valeur: int, compris entre 0 et 20 inclusivement et représentant le nombre de points associé au jeton.
    """
    def __init__(self, lettre, valeur):
        """
        Constructeur de la classe. Permet de créer un Jeton à partir d'une lettre et d'un nombre de points
        :param lettre: str, représentant la lettre écrite sur le jeton.
        :param valeur: int, > 0 représentant le nombre de points associé au jeton.
        :exception: Levez une exception avec assert si la valeur ne respecte pas
        la condition suivante 0 <= valeur <= 20 ou si la lettre n'est pas en majuscule.
        """
        assert 0 <= valeur <= 20, "La valeur est inférieur à 0 ou supérieure à 20."
        assert len(lettre) == 1 and lettre.isupper() and lettre.isalpha(), "Lettre incorrecte."

        self.lettre = lettre
        self.valeur = valeur

    def __str__(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Formatage d'un jeton. Cette méthode est appelée lorsque vous faites str(v) où v est un jeton.
        :return: str, correspondant au formatage du jeton.
        """
        if self.valeur < 10:
            res = "{}{}".format(self.lettre, chr(0x2080 + self.valeur))
        else:
            res = "{}{}{}".format(self.lettre, chr(0x2080 + int(self.valeur/10)), chr(0x2080 + int(self.valeur%10)))
        return res
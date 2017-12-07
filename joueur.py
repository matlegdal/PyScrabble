from random import shuffle
from exception import *

class Joueur:
    """
    Cette classe permet de représenter un joueur.

    La classe joueur possède une variable de classe:
    - TAILLE_CHEVALET : le nombre de jetons maximum qu'un joueur peut avoir.

    Un joueur a 3 attributs:
    - nom (str, public): représente le nom du joueur doit être non vide.
    - __points (entier, privé): représente le nombre de points que le joueur détient.
    - __chevalet (list, privé): représente le chevalet (l'ensemble des jetons du joueur) du joueur.
            Cette liste devrait être en tout temps de taille Joueur.TAILLE_CHEVALET.
            À chaque position du chevalier on peut avoir un jeton ou pas.
            Une position libre devra contenir None. Autrement elle devrait avoir un objet Jeton à cette position.
    """
    TAILLE_CHEVALET = 7

    def __init__(self, nom):
        """
        Initialise un objet joueur avec le nom passé en argument.
        Le nombre de points d'un joueur devra être 0 à l'initialisation, et le chevalet devra être vide.
        Rappel: Un chevalet vide veut dire une liste contenant que des None.
        :param nom: Le nom du joueur.
        :return: Ne retourne rien.
        :exception: Levez une exception si le nom est une chaine vide.
        """
        if nom == '' and nom.isspace():
            raise NomInvalideException("Entrez un nom valide. Minimum 1 caractère.")

        self.nom = nom
        self.__points = 0
        self.__chevalet = [None for _ in range(Joueur.TAILLE_CHEVALET)]
        self.jeton_actif = None
        self.jetons_jetes = []


    @property
    def nb_a_tirer(self):
        """
        Méthode permet de trouver le nombre de places vides dans le chevalet.
        Rappel: Un chevalet vide veut dire une liste contenant que des None.
        :return: (int) Le nombre de places vides dans le chevalet.
        """
        return self.__chevalet.count(None)

    @property
    def points(self):
        """
        Méthode permettant d'obtenir le nombre de points du joueur.
        :return: (int) Le nombre de points du joueur.
        """
        return self.__points

    @property
    def chevalet(self):
        """
        Méthode permettant d'obtenir le chevalet du joueur
        :return: (List) Liste des jetons du joueur
        """
        return self.__chevalet

    @staticmethod
    def position_est_valide(pos):
        """
        Méthode permettant de vérifier si une position sur un chevalet est valide ou pas.
        Valide veut dire que la position est entre 0 et Joueur.TAILLE_CHEVALET (Joueur.TAILLE_CHEVALET étant exclus)
        :param pos: (int) la position à valider
        :return: True si position valide, False sinon
        """
        return pos in range(Joueur.TAILLE_CHEVALET)

    def position_est_vide(self, pos):
        """
        Étant donnée une position sur le chevalet, cette méthode permet de voir
        si la position est vide ou pas.
        Rappel: Une position vide ne contient pas de jeton, juste None.
        :param pos: (int) position à vérifier.
        :return: True si la position est vide et False sinon.
        :exception: Levez une exception avec assert si la position n'est pas valide. Pensez à réutiliser Joueur.position_est_valide.
        """
        if not Joueur.position_est_valide(pos):
            raise PositionChevaletException("La position du chevalet n'est pas valide")

        return self.__chevalet[pos] is None

    def ajouter_jeton(self, jeton, pos=None):
        """
        Étant donnés un jeton et une position sur le chevalet, cette méthode permet d'ajouter le jeton
        au chevalet si la position mentionnée est vide.
        Si la position est vide (i.e. pos est égal à None), le jeton est mis à la première position libre du chevalet
        en partant de la gauche.
        Rappel: Une position vide ne contient pas de jeton, juste None.
        :param jeton: (Jeton) Jeton à placer sur le chevalet.
        :param pos: (int, optionnel) Position où ajouter le jeton.
        :return: Ne retourne rien.
        :exception: Levez une exception avec assert si la position est spécifiée mais n'est pas valide ou si elle n'est
                    pas vide pour y déposer un jeton. Pensez à réutiliser Joueur.position_est_valide et position_est_vide.
                    On lève aussi une exception si la position n'est pas spécifiée, mais il n'y a pas de place vide dans le chevalet
        """
        # Si la position est spécifiée, on place le jeton à cette position
        if pos is not None:
            if not self.position_est_vide(pos):
                raise PositionChevaletException("La position du chevalet n'est pas vide")
            self.__chevalet[pos] = jeton
        # Sinon, on la place au premier index disponible. On lève une exception s'il n'y a pas de place disponible
        else:
            if None not in self.__chevalet:
                raise PositionChevaletException("Il n'y a pas de place vide dans le chevalet")
            self.__chevalet[self.__chevalet.index(None)] = jeton

    def retirer_jeton(self, pos):
        """
        Cette méthode permet de retirer un jeton du chevalet: c'est comme simuler un joueur qui prend un jeton de son chevalet.
        Donc retirer veut dire mettre la position à None et retourner le jeton qui était présent à cet emplacement.
        :param pos: Position du jeton à retirer.
        :return: Le jeton retiré.
        :exception: Levez une exception avec assert si la position spécifiée n'est pas valide ou si elle est vide.
                    Pensez à réutiliser Joueur.position_est_valide et position_est_vide.
        """
        if self.position_est_vide(pos):
            raise PositionChevaletException("La position du chevalet indiquée est vide.")
        jeton_retire = self.__chevalet[pos]
        self.__chevalet[pos] = None
        return jeton_retire

    def obtenir_jeton(self, pos):
        """
        Cette méthode permet d'obtenir un jeton du chevalet: c'est comme si le joueur voulait voir un jeton de son chevalet.
        Donc obtenir un jeton à une position revient juste à retourner le jeton à la position indiquée.
        :param pos: Position du jeton.
        :return: Le jeton à la position d'intérêt.
        :exception: Levez une exception avec assert si la position spécifiée n'est pas valide ou si elle est vide.
                    Pensez à réutiliser Joueur.position_est_valide et position_est_vide.
        """
        if self.position_est_vide(pos):
            raise PositionChevaletException("La position du chevalet indiquée est vide.")
        return self.__chevalet[pos]

    def ajouter_points(self, points):
        """
        Cette méthode permet d'ajouter des points à un joueur
        :param points: (int) points à ajouter.
        :return: Ne retourne rien.
        """
        self.__points += points

    def melanger_jetons(self):
        """
        Cette méthode permet de mélanger au hasard le chevalet du joueur, c'est-à-dire mélanger les positions des éléments
        dans la liste représentant le chevalet.
        Pensez à utiliser la fonction shuffle du module random.
        :return: Ne retourne rien.
        """
        shuffle(self.__chevalet)


# Tests
if __name__ == '__main__':

    # valide init
    joueur = Joueur('Joueur 1')
    assert joueur.points == 0
    assert joueur.nb_a_tirer == 7

    # valide la position et case est vide
    assert joueur.position_est_valide(0) and joueur.position_est_valide(6)
    assert not joueur.position_est_valide(7)
    assert joueur.position_est_vide(0)

    # valide l'ajout de jetons
    joueur.ajouter_jeton('jeton1')
    assert not joueur.position_est_vide(0) and joueur.nb_a_tirer == 6
    joueur.ajouter_jeton('jeton2', 3)
    assert not joueur.position_est_vide(3) and joueur.nb_a_tirer == 5

    # teste l'assert dans ajouter_jeton() qui teste s'il y a une place vide
    # for _ in range(joueur.nb_a_tirer):
    #     joueur.ajouter_jeton('jeton')
    # joueur.ajouter_jeton('jeton') nous donne une assertion error

    # valide le retrait de jetons
    jet = joueur.retirer_jeton(3)
    assert joueur.position_est_vide(3) and joueur.nb_a_tirer == 6
    assert jet == 'jeton2'

    # valide l'obtention de jeton
    assert joueur.obtenir_jeton(0) == 'jeton1'

    # valide l'ajout de points
    joueur.ajouter_points(5)
    assert joueur.points == 5
    joueur.ajouter_points(3)
    assert joueur.points == 8

import pickle
from random import randint, shuffle, seed
from joueur import Joueur
from jeton import Jeton
from plateau import Plateau
from utils import *
from tkinter import *
from tkinter import messagebox
from exception import *
from math import floor


class Scrabble(Tk):
    """
    Classe Scrabble qui implémente aussi une partie de la logique de jeu.

    Les attributs d'un scrabble sont:
    - dictionnaire: set, contient tous les mots qui peuvent être joués sur dans cette partie.
    En gros pour savoir si un mot est permis on va regarder dans le dictionnaire.
    - plateau: Plateau, un objet de la classe Plateau on y place des jetons et il nous dit le nombre de points gagnés.
    - jetons_libres: Jeton list, la liste de tous les jetons dans le sac, c'est là que chaque joueur
                    peut prendre des jetons quand il en a besoin.
    - joueurs: Joueur list,  L'ensemble des joueurs de la partie.
    - joueur_actif: Joueur, le joueur qui est entrain de jouer le tour en cours. Si aucun joueur alors None.
    """
    PIXELS_PAR_CASE = 40

    def __init__(self):
        super().__init__()

        # Declare parameters
        self.liste_langue = ['FR', 'EN']
        self.title("Scrabble")
        self.plateau = None
        self.joueur_actif = None
        self.joueurs = []
        self.jetons_libres = []
        self.dictionnaire = None
        self.message = StringVar()
        self.nom_joueur = StringVar()
        self.pointage = StringVar()
        self.chevalet_actif = None
        self.debut = True


        # Configure
        self.content = Frame(self)
        self.content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW, padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(width=800, height=600)

        self.content.grid_columnconfigure(0, weight=2)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=2)

        # Création du menu
        barre_menu = Menu(self)
        fichier = Menu(barre_menu, tearoff=0)
        fichier.add_command(label="Nouvelle partie", command=Scrabble)
        fichier.add_command(label="Sauvegarder la partie", state=DISABLED)  # TODO: implanter sauvegarder_partie()
        fichier.add_command(label="Charger une partie", state=DISABLED)  # TODO: commande qui ouvre une fenetre avec un text pour charger la partie
        fichier.add_separator()
        fichier.add_command(label="Quitter", command=self.quit)
        barre_menu.add_cascade(label="Fichier", menu=fichier)

        aide = Menu(barre_menu, tearoff=0)
        aide.add_command(label="Règlements", state=DISABLED)  # TODO: faire apparaître une fenêtre avec les règlements ->
        barre_menu.add_cascade(label="Aide", menu=aide)

        self.config(menu=barre_menu)

        # On appelle l'écran d'accueil
        self.accueil()


    def accueil(self):
        accueil = Frame(self.content)
        accueil.grid(row=0, column=0, rowspan=2, columnspan=2)

        # message de bienvenue
        Label(accueil, text="Bienvenue dans IFT-1004 Scrabble", font=("Times", 24)).grid(row=0, columnspan=4)
        # label de la langue
        Label(accueil, text="Choisissez la langue du jeu:", font=("Times", 16)).grid(row=1, columnspan=4)

        # Choix des langues
        langue = StringVar()
        langue.set('FR')
        Radiobutton(accueil, text='Français', variable=langue, value='FR').grid(column=0, row=2, columnspan=2, sticky=E)
        Radiobutton(accueil, text='English', variable=langue, value='EN').grid(column=2, row=2, columnspan=2, sticky=W)

        # Nombre des joueurs
        Label(accueil, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=3, column=0, columnspan=4)
        nb_joueurs = IntVar()
        nb_joueurs.set(2)
        Radiobutton(accueil, text='2 joueurs', variable=nb_joueurs, value=2).grid(column=0, row=4)
        Radiobutton(accueil, text='3 joueurs', variable=nb_joueurs, value=3).grid(column=1, row=4)
        Radiobutton(accueil, text='4 joueurs', variable=nb_joueurs, value=4).grid(column=2, row=4)
        Radiobutton(accueil, text='Jouer contre l\'ordinateur', variable=nb_joueurs, value=1, state=DISABLED).grid(column=3, row=4)

        # Débuter la partie
        Button(accueil, text="Commencer la partie", command=lambda: self.demarrer_partie(accueil, nb_joueurs.get(), langue.get())).grid(row=5, column=0, columnspan=4)


    def demarrer_partie(self, accueil, nb_joueurs, langue):
        """
        Démarre une partie en détruisant la page d'accueil, initialisant la partie et passe le contrôle à jouer().
        :param accueil: (Frame) Page d'accueil
        :param nb_joueurs: (int) Nombre de joueurs
        :param langue: (str) Code de langue à 2 lettres
        :return: aucun return
        """
        accueil.destroy()
        self.initialiser_partie(nb_joueurs, langue)
        self.jouer()
        self.changer_joueur()


    def initialiser_partie(self, nb_joueurs, langue):
        """
        - La liste des joueurs est créée et chaque joueur porte automatiquement le nom Joueur 1, Joueur 2, ... Joueur n où n est le nombre de joueurs;
        - Le sac à jetons (self.jetons_libres) est créé
        - Le dictionnaire est ouvert

        :param nb_joueurs: int, nombre de joueurs de la partie au minimun 2 au maximum 4.
        :param langue: str, FR pour la langue française, et EN pour la langue anglaise. Dépendamment de la langue, vous devez ouvrir, lire, charger en mémoire le fichier "dictionnaire_francais.txt" ou "dictionnaire_anglais.txt" ensuite il faudra ensuite extraire les mots contenus pour construire un set avec le mot clé set.
        Aussi, grâce à la langue vous devez être capable de créer tous les jetons de départ et les mettre dans jetons_libres.
        Pour savoir combien de jetons créés pour chaque langue vous pouvez regarder à l'adresse:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
        *** Dans notre scrabble, nous n'utiliserons pas les jetons jokers qui ne contienent aucune lettre donc ne les incluez pas dans les jetons libres ***
        :exception: Levez une exception avec assert si la langue n'est ni fr, FR, en, ou EN ou si nb_joueur < 2 ou > 4.
        """
        assert 2 <= nb_joueurs <= 4
        assert langue.upper() in self.liste_langue

        self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]

        if langue.upper() == 'FR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 15, 1), ('A', 9, 1), ('I', 8, 1), ('N', 6, 1), ('O', 6, 1),
                    ('R', 6, 1), ('S', 6, 1), ('T', 6, 1), ('U', 6, 1), ('L', 5, 1),
                    ('D', 3, 2), ('M', 3, 2), ('G', 2, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 8), ('K', 1, 10), ('W', 1, 10), ('X', 1, 10), ('Y', 1, 10),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_francais.txt'
        elif langue.upper() == 'EN':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('N', 6, 1), ('O', 8, 1),
                    ('R', 6, 1), ('S', 4, 1), ('T', 6, 1), ('U', 4, 1), ('L', 4, 1),
                    ('D', 4, 2), ('M', 2, 3), ('G', 3, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 10), ('K', 1, 5), ('W', 2, 4), ('X', 1, 8), ('Y', 2, 4),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_anglais.txt'

        # TODO: refactor -> mettre les jetons (data) dans des fichiers à part (pour pouvoir ajouter des langues facilement)

        self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for _ in range(occurences)]
        with open(nom_fichier_dictionnaire, 'r') as f:
            self.dictionnaire = set([x[:-1].upper() for x in f.readlines() if len(x[:-1]) > 1])



    def jouer(self):
        """
        La fonction démarre une partie de scrabble.
        Pour une nouvelle partie de scrabble,
        - un nouvel objet Plateau est créé;
        - Affiche le pointage
        - Affiche le message du tour en cours
        - Crée le Canvas du chevalet
        - Affiche les boutons d'actions
        """

        # Set le plateau
        self.plateau = Plateau(self.content, self.PIXELS_PAR_CASE)
        self.plateau.grid(row=0, column=0, rowspan=2, columnspan=1, sticky=NSEW)
        # self.plateau.tag_bind('case', '<Button-1>', self.poser_jeton)

        # Set les joueurs
        affichage_joueur = Frame(self.content)
        affichage_joueur.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=NSEW)

        # self.nom_joueur.set(self.joueur_actif)
        Label(affichage_joueur, textvariable=self.nom_joueur).grid(row=0, column=0, columnspan=4)

        self.chevalet_actif = Canvas(affichage_joueur, height=self.PIXELS_PAR_CASE, width=self.PIXELS_PAR_CASE*Joueur.TAILLE_CHEVALET, bg='#f5ebdc')
        self.chevalet_actif.grid(row=1, column=0, columnspan=4, sticky=NSEW)

        # Set le tableau d'affichange
        tableau = Frame(self.content)
        tableau.grid(row=0, column=1, sticky=NSEW)
        Label(tableau, textvariable=self.message).grid(row=0)
        Label(tableau, textvariable=self.pointage).grid(row=1)

        # Set les boutons d'actions
        btn_jouer = Button(affichage_joueur, text="Joueur le tour", command=self.jouer_tour)
        btn_passer = Button(affichage_joueur, text="Passer le tour", command=self.changer_joueur)
        btn_changer = Button(affichage_joueur, text="Changer les jetons")
        btn_quitter = Button(affichage_joueur, text="Quitter la partie", command=self.quitter)

        # Affichage des boutons d'actions
        btn_jouer.grid(row=2, column=0, columnspan=4, sticky=NSEW, pady=30)
        btn_passer.grid(row=3, column=0)
        btn_changer.grid(row=3, column=1)
        btn_quitter.grid(row=3, column=2)


    def dessiner_chevalet(self, master, joueur):
        """
        Cette fonction dessine le chevalet du joueur actif dans un canevas.
        :param master: (obj Canvas) Le canvas parent.
        :param joueur: (obj Joueur) Joueur actif
        :return: Aucun
        """
        assert isinstance(master, Canvas)
        assert isinstance(joueur, Joueur)

        for pos in range(Joueur.TAILLE_CHEVALET):
            if joueur.chevalet[pos] is None:
                continue

            x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)
            dessiner_jeton(master, x1, y1, x2, y2, delta, joueur.chevalet[pos], ('chevalet', 'chevalet{}'.format(pos)))


    def msg_points(self):
        """
        Cette fonction sert à formatter les points de tous les joueurs pour l'afficher dans le tableau
        :return: (str) Chaine de charactères formattée montrant les points de tous les joueurs
        """
        msg_points = ""
        for joueur in self.joueurs:
            msg_points += "{}:{} ".format(joueur.nom, joueur.points)

        return msg_points

    def determiner_case(self, event):
        """
        Permet de déterminer la case clickée par un event de souris
        :param event: l'event de souris
        :return: (tuple) tuple à 3 éléments: ligne du plateau, colonne du plateau, case
        """
        ligne = floor(event.y / self.plateau.pixels_par_case)
        col = floor(event.x / self.plateau.pixels_par_case)

        if 0 > ligne >= self.plateau.DIMENSION or 0 > col >= self.plateau.DIMENSION:
            raise PositionInvalideException("La position est invalide")

        return ligne, col, self.plateau.cases[ligne][col]

    def poser_jeton(self, event):
        """
        Event handler des cases du plateau.
        - Vérifier que la position est valide et que la case est vide.
        - Placer le jeton dans la case
        - Dessiner le jeton dans la case.
        - Ajouter la case à la liste des positions à vérifier
        - Ajouter le jeton à la liste des jetons placés
        - Unbind redeposer et met jeton_actif à None
        """
        ligne, col, case = self.determiner_case(event)
        try:
            case.placer_jeton(self.joueur_actif.jeton_actif)
            self.plateau.positions.append((ligne, col))
            self.plateau.jetons_places.append(self.joueur_actif.jeton_actif)

            x1, y1, x2, y2, delta = coord_case(ligne, col, self.plateau.pixels_par_case)
            dessiner_jeton(self.plateau, x1, y1, x2, y2, delta, self.joueur_actif.jeton_actif, ('jeton_place', "jeton_{}_{}".format(ligne, col)))

            self.joueur_actif.jeton_actif = None

            self.unbind_redeposer()
            self.after(500, self.bind_reprendre)
        except (CaseOccupeeException, AssertionError) as e:
            print(e) # TODO: améliorer la gestion des erreurs!


    def reprendre_jeton(self, event):
        """
        Permet de reprendre un jeton déposé sur le plateau par le joueur.
        - Retirer le jeton de la case
        - Effacer le jeton du plateau
        - Enlever la case et le jeton des listes cases_placees et jetons_places
        - Binder redéposer
        """
        ligne, col, case = self.determiner_case(event)

        # TODO: s'assurer que le joueur ne peut reprendre que les jetons placés au cours de son tour.
        if self.joueur_actif.jeton_actif is None:
            try:
                jeton = case.retirer_jeton()
                self.plateau.delete("jeton_{}_{}".format(ligne, col))

                self.plateau.jetons_places.remove(jeton)
                self.joueur_actif.jeton_actif = jeton
                self.plateau.positions.remove((ligne, col))

                self.bind_redeposer()
            except CaseVideException as e:
                print(e)


    def prendre_jeton(self, event):
        """
        Gère l'évènement d'un clique de souris sur un jeton du chevalet.
        - Retirer le jeton du chevalet
        - Met le jeton retiré dans la variable jeton_actif du joueur.
        - Retirer le visuel du jeton du chevalet_actif
        - Activer le event handler pour redeposer le jeton sur le chevalet
        - Activer le event handler pour poser le jeton sur le plateau
        :param event: évènement du clic de la souris. Inclus la position en x,y sur le canevas.
        :return: Aucun retour
        """
        if self.joueur_actif.jeton_actif is None:
            pos = floor(event.x / self.PIXELS_PAR_CASE)
            try:
                self.joueur_actif.jeton_actif = self.joueur_actif.retirer_jeton(pos)

                assert isinstance(self.joueur_actif.jeton_actif, Jeton)
                assert self.joueur_actif.chevalet[pos] is None

                self.chevalet_actif.delete('chevalet{}'.format(pos))

                self.after(500, self.bind_redeposer)
                self.plateau.tag_bind('case', '<Button-1>', self.poser_jeton)
            except (PositionChevaletException, AssertionError) as e:
                print(e)

        # TODO: à compléter -> ajouter l'image du jeton qui suit la souris genre drag-drop

    def bind_reprendre(self):
        """
        Fonction utilitaire pour binder le clic de souris aux jetons placés.
        """
        self.plateau.tag_bind('jeton_place', '<Button-1>', self.reprendre_jeton)

    def bind_redeposer(self):
        """
        Fonction utilitaire pour binder le clic de souris au chevalet. Utilisé pour éviter que les événements de prendre un jeton
        et de redéposer un jeton ne soient déclenchés par le même clic de souris.
        """
        self.chevalet_actif.bind('<Button-1>', self.redeposer_jeton)

    def unbind_redeposer(self):
        """
        Fonction utilitaire pour unbinder le clic de souris au chevalet. Utilisé pour éviter que les événements de prendre un jeton
        et de redéposer un jeton ne soient déclenchés par le même clic de souris.
        """
        self.chevalet_actif.bind('<Button-1>', lambda e: "break")

    def redeposer_jeton(self, event):
        """
        Gère l'évènement de redéposer le jeton actif dans le chevalet.
        - Désactiver le event-handler de redeposer
        - Ajouter le jeton au chevalet
        - Dessiner le jeton
        - Mettre le jeton_actif à None
        :param event: Évènement du clic de la souris. Non-utilisé
        :return: Aucun retour
        """
        self.unbind_redeposer()
        if self.joueur_actif.jeton_actif is not None:
            try:
                pos = self.joueur_actif.chevalet.index(None)
                self.joueur_actif.ajouter_jeton(self.joueur_actif.jeton_actif, pos)

                x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)

                dessiner_jeton(self.chevalet_actif, x1, y1, x2, y2, delta,self.joueur_actif.jeton_actif, ('chevalet', 'chevalet{}'.format(pos)))
                self.joueur_actif.jeton_actif = None

            except PositionChevaletException as e:
                print(e)

    def jouer_tour(self):
        """
        Permet à un joueur de jouer un tour. La fonction vérifie que les mots placés sont acceptés et met à jour les scores.
        Si les mots sont corrects, on change de joueur, sinon on retourne les jetons dans le chevalet et le joueur peut continuer à tenter des mots.
        - Vérifier la validité des mots placés
        - Calculer les mots et le score obtenus
        - Ajouter les points au joueur
        - Resetter les listes de positions et jetons placés
        - changer de joueur
        :return: Aucun return
        """
        try:
            self.plateau.valider_positions(self.plateau.positions)
        except (CasesNonEnLigneException, PasDeCasesAdjacentes, CaseVideDansMot) as e:
            print(e)
            # TODO: implanter la bonne exception -> retourner jetons

        else:
            mots, score = self.plateau.mots_score_obtenus(self.plateau.positions)

            if any([not self.mot_permis(m) for m in mots]):
                pass
                # TODO: à compléter la vérification des mots dans le dictionnaire. On peut s'inspirer de ci-dessous la fonction ancienne...
                # print("Au moins l'un des mots formés est absent du dictionnaire.")
                # for pos in pos_plateau:
                #      jeton = self.plateau.retirer_jeton(pos)
                #      self.joueur_actif.ajouter_jeton(jeton)
                #      valide = False


            self.joueur_actif.ajouter_points(score)
            self.plateau.positions = []
            self.plateau.jetons_places = []

            self.changer_joueur()


    def mot_permis(self, mot):
        """
        Permet de savoir si un mot est permis dans la partie ou pas en regardant dans le dictionnaire.
        :param mot: str, mot à vérifier.
        :return: bool, True si le mot est dans le dictionnaire, False sinon.
        """
        return mot.upper() in self.dictionnaire

    def determiner_gagnant(self):
        """
        Détermine le joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        il doit avoir le pointage le plus élevé de tous.

        :return: Joueur, un des joueurs gagnants, i.e si plusieurs sont à égalité on prend un au hasard.
        """
        # On trouve le maximum de points
        max_points = max([joueur.points for joueur in self.joueurs])
        # On sélectionne les joueurs ayant le nombre max de points
        joueurs_gagnants = [joueur for joueur in self.joueurs if joueur.points == max_points]
        # On shuffle la liste ce qui permet de retourner un joueur au hasard.
        shuffle(joueurs_gagnants)
        return joueurs_gagnants[0]

    def partie_terminee(self):
        """
        Vérifie si la partie est terminée. Une partie est terminée s'il n'existe plus de jetons libres ou il reste moins de deux (2) joueurs.
        C'est la règle que nous avons choisi d'utiliser pour ce travail, donc essayez de négliger les autres que vous connaissez ou avez lu sur Internet.
        :return: bool, True si la partie est terminée, et False autrement.
        """
        return len(self.jetons_libres) < 1 or len(self.joueurs) < 2

    def joueur_suivant(self):
        """
        Change le joueur actif.
        Le nouveau joueur actif est celui à l'index du (joueur courant + 1)% nb_joueurs.
        Si on n'a aucun joueur actif, on détermine au hasard le suivant.
        :return: aucun return
        """
        if self.joueur_actif is None:
            self.joueur_actif = self.joueurs[randint(0, len(self.joueurs)-1)]
        else:
            self.joueur_actif = self.joueurs[(self.joueurs.index(self.joueur_actif)+1) % len(self.joueurs)]

    def changer_joueur(self):
        """
        Change le joueur. C'est l'action de passer le tour au prochain joueur. La méthode change le joueur actif et affiche dans l'interface les infos du nouveau joueur.
        La méthode vérifie aussi si la partie est terminée.
        :return: Aucun return
        """
        if self.partie_terminee():
            messagebox.showinfo('Partie terminée', '{} est le gagnant! Félicitations!'.format(self.determiner_gagnant().nom))
            # TODO: vérifier pour cette condition si l'exécution se fait bien et potentiellement améliorer l'action

        self.joueur_suivant()

        if self.debut:
            msg = "La partie va commencer avec le {}".format(self.joueur_actif.nom)
            self.debut = False
        else:
            msg = "C'est le tour de {}".format(self.joueur_actif.nom)
        self.message.set(msg)
        self.pointage.set(self.msg_points())
        self.nom_joueur.set(self.joueur_actif.nom)

        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)
        self.dessiner_chevalet(self.chevalet_actif, self.joueur_actif)
        self.chevalet_actif.tag_bind('chevalet', '<Button-1>', self.prendre_jeton)


    def quitter(self):
        """
        Retire un joueur de la liste des joueurs
        :return: Aucun return
        """
        quitter = self.joueur_actif
        self.changer_joueur()
        self.joueurs.remove(quitter)

    def changer_jetons(self):
        """
        Change les jetons du joueur actif.
        :return: Aucun return
        :exception: Lever une exception si le nombre de jetons à changer est supérieur au nombre de jetons restants.
        """
        #TODO: à compléter, on peut s'inspirer de l'ancienne méthode, mais il y a bcp à changer

    def tirer_jetons(self, n):
        """
        Simule le tirage de n jetons du sac à jetons et renvoie ceux-ci. Il s'agit de prendre au hasard des jetons dans self.jetons_libres et de les retourner.
        Pensez à utiliser la fonction shuffle du module random.
        :param n: le nombre de jetons à tirer.
        :return: Jeton list, la liste des jetons tirés.
        :exception: Levez une exception avec assert si n ne respecte pas la condition 0 <= n <= 7.
        """
        assert 0 <= n <= len(self.jetons_libres), "n doit être compris entre 0 et le nombre total de jetons libres."

        # On mélange les jetons dans le sac
        shuffle(self.jetons_libres)

        # On prend n jetons et on les enlève du sac
        jetons_tires = self.jetons_libres[:n]
        self.jetons_libres = self.jetons_libres[n:]

        # On retourne les jetons tirés
        return jetons_tires

    # def demander_positions(self):
    #     """ *** Vous n'avez pas à coder cette méthode ***
    #     Demande à l'utilisateur d'entrer les positions sur le chevalet et le plateau
    #     pour jouer son coup.
    #     Si les positions entrées sont valides, on retourne les listes de ces positions. On doit
    #     redemander tant que l'utilisateur ne donne pas des positions valides.
    #     Valide ici veut dire uniquement dans les limites donc pensez à utilisez valider_positions_avant_ajout et Joueur.position_est_valide.
    #
    #     :return: tuple (int list, str list): Deux listes, la première contient les positions du chevalet (plus précisement il s'agit des indexes de ces positions) et l'autre liste contient les positions codées du plateau.
    #     """
    #     # Cette méthode devrait être décomposée en 2 méthodes: demander_positions_chevalet() et demander_positions_cases()
    #     # En effet une méthode devrait faire une seule chose, pas deux comme c'est le cas ici.
    #     valide = False
    #     while not valide:
    #         input_pos_chevalet = input("Entrez les positions du chevalet à jouer séparées par un espace: ").upper().strip()
    #         pos_chevalet = [int(x) - 1 for x in input_pos_chevalet.split(' ')]
    #         valide = all([Joueur.position_est_valide(pos) for pos in pos_chevalet])
    #
    #     valide = False
    #     while not valide:
    #         input_pos_plateau = input("Entrez les cases de chacune de ces lettres séparées par un espace: ").upper().strip()
    #         pos_plateau = input_pos_plateau.split(' ')
    #
    #         if len(pos_chevalet) != len(pos_plateau):
    #             print("Les nombres de jetons et de positions ne sont pas les mêmes.")
    #             valide = False
    #         else:
    #             # Nous avons refactorée cette partie pour pouvoir afficher un message d'erreur plutôt que juste re-prompter le joueur sans rien dire.
    #             # ligne originale:
    #             # valide = self.plateau.valider_positions_avant_ajout(pos_plateau)
    #             if self.plateau.valider_positions_avant_ajout(pos_plateau):
    #                 valide = True
    #             else:
    #                 print("""Les cases spécifiées ne sont pas valides.
    #                 Les positions sont valides si:
    #                     - elles sont toutes vides;
    #                     - elles sont toutes sur la même ligne ou la même colonne;
    #                     - si le plateau est vide, le centre du plateau (H8) doit être dans les positions;
    #                     - sinon, au moins une des positions doit être adjacente à une des cases occupées
    #                       du plateau""""")
    #
    #     return pos_chevalet, pos_plateau

    # def jouer_un_tour(self):
    #     """
    #     Faire jouer à un des joueurs son tour entier jusqu'à ce qu'il place un mot valide sur le
    #     plateau.
    #     Pour ce faire
    #     1 - Afficher le plateau puis le joueur;
    #     2 - Demander les positions à jouer;
    #     3 - Retirer les jetons du chevalet;
    #     4 - Valider si les positions sont valides pour un ajout sur le plateau;
    #     5 - Si oui, placer les jetons sur le plateau, sinon retourner en 1;
    #     6 - Si tous les mots formés sont dans le dictionnaire, alors ajouter les points au joueur actif;
    #     7 - Sinon retirer les jetons du plateau et les remettre sur le chevalet du joueur, puis repartir en 1;
    #     8 - Afficher le plateau.
    #
    #     :return: Ne retourne rien.
    #     """
    #     print(self.plateau)
    #     print(self.joueur_actif)
    #
    #     # Nous avons modifié légèrement la méthode fournie pour la rendre beaucoup plus robuste et éviter la fin abrupte du programme.
    #     # La seule modification est l'ajout de boucles incluant un try/except pour valider les inputs.
    #     valide = False
    #     while not valide:
    #         while True:
    #             try:
    #                 pos_chevalet, pos_plateau = self.demander_positions()
    #                 break
    #             except (AssertionError, ValueError) as e:
    #                 print(e)
    #                 continue
    #
    #         jetons = [self.joueur_actif.retirer_jeton(p) for p in pos_chevalet]
    #
    #         while True:
    #             try:
    #                 mots, score = self.plateau.placer_mots(jetons, pos_plateau)
    #                 break
    #             except AssertionError as e:
    #                 print(e)
    #                 continue
    #
    #         if any([not self.mot_permis(m) for m in mots]):
    #             print("Au moins l'un des mots formés est absent du dictionnaire.")
    #             for pos in pos_plateau:
    #                 jeton = self.plateau.retirer_jeton(pos)
    #                 self.joueur_actif.ajouter_jeton(jeton)
    #             valide = False
    #         else:
    #             print("Mots formés:", mots)
    #             print("Score obtenu:", score)
    #             self.joueur_actif.ajouter_points(score)
    #             valide = True
    #
    #     print(self.plateau)
    #
    # def changer_jetons(self):
    #     """
    #     Faire changer au joueur actif ses jetons. La méthode doit demander au joueur de saisir les positions à changer les unes après les autres séparés par un espace.
    #     Si une position est invalide (utilisez Joueur.position_est_valide) alors redemander.
    #     Dès que toutes les positions valides les retirer du chevalier du joueur et lui en donner de nouveau.
    #     Enfin, on remet des jetons pris chez le joueur parmi les jetons libres.
    #     :return: Ne retourne rien.
    #     """
    #     print(self.joueur_actif)
    #     # On demande au joueur de saisir les positions du chevalet à changer
    #     valide = False
    #     while not valide:
    #         try:
    #             input_pos_chevalet = input("Entrez les positions du chevalet à changer séparées par un espace: ").strip()
    #             pos_chevalet = [int(pos) - 1 for pos in input_pos_chevalet.split(' ')]
    #
    #             # On vérifie que toutes les positions du chevalet fournies ont un jeton (pas vides)
    #             valide = all([not self.joueur_actif.position_est_vide(pos) for pos in pos_chevalet])
    #
    #             # Si le nb de jetons à changer excède le nb de jetons dispo dans le sac, on lève une exception
    #             if len(pos_chevalet) > len(self.jetons_libres):
    #                 raise AssertionError("Le nombre de jeton à changer excède le nombre de jetons restants dans le sac à jetons.")
    #         except (AssertionError, ValueError) as e:
    #             print(e)
    #             continue
    #
    #     # On retire les jetons désirés et on les place dans la liste des jetons retirés
    #     jetons_retires = [self.joueur_actif.retirer_jeton(pos) for pos in pos_chevalet]
    #
    #     # On pige les nouveaux jetons dans le sac à jetons et on les ajoute au chevalet du joueur
    #     jetons_a_ajouter = self.tirer_jetons(self.joueur_actif.nb_a_tirer)
    #     for jeton in jetons_a_ajouter:
    #         self.joueur_actif.ajouter_jeton(jeton)
    #
    #     # On retourne les jetons retirés du joueur dans le sac à jeton
    #     self.jetons_libres = self.jetons_libres + jetons_retires
    #
    #     print("Nouveau plateau du", self.joueur_actif)

    # def jouer(self):
    #     """
    #     Cette fonction permet de jouer la partie.
    #     Tant que la partie n'est pas terminée, on joue un tour.
    #     À chaque tour :
    #         - On change le joueur actif et on lui affiche que c'est son tour. ex: Tour du joueur 2.
    #         - On lui affiche ses options pour qu'il choisisse quoi faire:
    #             "Entrez (j) pour jouer, (p) pour passer votre tour, (c) pour changer certains jetons,
    #             (s) pour sauvegarder ou (q) pour quitter"
    #         Notez que si le joueur fait juste sauvegarder on ne doit pas passer au joueur suivant mais dans tous les autres cas on doit passer au joueur suivant.
    #         S'il quitte la partie on l'enlève de la liste des joueurs.
    #     Une fois la partie terminée, on félicite le joueur gagnant!
    #
    #     :return Ne retourne rien.
    #     """
    #     abandon = False
    #     changer_joueur = True
    #     while not self.partie_terminee() and not abandon:
    #         debut = self.joueur_actif is None
    #         if changer_joueur:
    #             self.joueur_suivant()
    #         if debut:
    #             self.message = "Le premier joueur sera: {}.".format(self.joueur_actif.nom)
    #
    #         for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
    #             self.joueur_actif.ajouter_jeton(jeton)
    #
    #         self.message = "Tour du {}.".format(self.joueur_actif.nom)
            # choix = ''
            # while choix not in ['j', 'p', 'c', 'q', 's']:
            #     choix = input("Entrez (j) pour jouer, (p) pour passer votre tour,\n"
            #                   "(c) pour changer certains jetons, (s) pour sauvegarder\n"
            #                   "ou (q) pour quitter: ").strip().lower()
            #     if choix == "j":
            #         self.jouer_un_tour()
            #         changer_joueur = True
            #     elif choix == "p":
            #         changer_joueur = True
            #     elif choix == "c":
            #         self.changer_jetons()
            #         changer_joueur = True
            #     elif choix == "q":
            #         quitter = self.joueur_actif
            #         self.joueur_suivant()
            #         self.joueurs.remove(quitter)
            #         changer_joueur = False
            #     elif choix == "s":
            #         valide = False
            #         while not valide:
            #             nom_fichier = input("Nom du fichier de sauvegarde: ")
            #             valide = self.sauvegarder_partie(nom_fichier)
            #         changer_joueur = False
            #     else:
            #         print('Erreur: Entrez un choix valide.')

        # if self.partie_terminee():
        #     print("Partie terminée.")
        #     print("{} est le gagnant. Félicitations!!!".format(self.determiner_gagnant().nom))

    def sauvegarder_partie(self, nom_fichier):
        """ *** Vous n'avez pas à coder cette méthode ***
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: True si la sauvegarde s'est bien passé, False si une erreur s'est passé durant la sauvegarde.
        """
        try:
            with open(nom_fichier, "wb") as f:
                pickle.dump(self, f)
        except:
            return False
        return True

    @staticmethod
    def charger_partie(nom_fichier):
        """ *** Vous n'avez pas à coder cette méthode ***
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment. Pensez à utiliser la fonction load du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: Scrabble, l'objet chargé en mémoire.
        """
        with open(nom_fichier, "rb") as f:
            objet = pickle.load(f)
        return objet


# if __name__ == '__main__':
#
#     scrabble = Scrabble()
#
# # mot_permis()
#     assert scrabble.mot_permis('car')
#     assert not scrabble.mot_permis('abc')
#
# # déterminer_gagnant
#     scrabble.joueurs[0].ajouter_points(1)
#     scrabble.joueurs[1].ajouter_points(5)
#     assert scrabble.determiner_gagnant() == scrabble.joueurs[1]
#
#     scrabble.joueurs[2].ajouter_points(5)
#     print(scrabble.determiner_gagnant().nom)
#
# # partie_terminee
#     assert not scrabble.partie_terminee()
#
#     scrabble.jetons_libres = []
#     assert scrabble.partie_terminee()
#
#     scrabble = Scrabble(2)
#     scrabble.joueurs.pop()
#     assert scrabble.partie_terminee()
#
# # joueur_actif
#     scrabble = Scrabble(2)
#     scrabble.joueur_suivant()
#     assert isinstance(scrabble.joueur_actif, Joueur)
#
#     scrabble.joueur_actif = scrabble.joueurs[0]
#     scrabble.joueur_suivant()
#     assert scrabble.joueur_actif == scrabble.joueurs[1]
#     scrabble.joueur_suivant()
#     assert scrabble.joueur_actif == scrabble.joueurs[0]
#
#     scrabble = Scrabble(4)
#     scrabble.joueur_actif = scrabble.joueurs[0]
#     scrabble.joueur_suivant()
#     scrabble.joueur_suivant()
#     scrabble.joueur_suivant()
#     assert scrabble.joueur_actif == scrabble.joueurs[3]
#     scrabble.joueur_suivant()
#     assert scrabble.joueur_actif == scrabble.joueurs[0]
#
# # tirer_jetons
#     assert len(scrabble.tirer_jetons(2)) == 2 and isinstance(scrabble.tirer_jetons(2)[0], Jeton)
#     nbr_jetons_libres = len(scrabble.jetons_libres)
#     scrabble.tirer_jetons(2)
#     assert len(scrabble.jetons_libres) == nbr_jetons_libres - 2


# changer jetons
    # ici dans le input on doit entrer manuellement.
    # ça serait possible de faire un test bcp plus robuste avec le module unittest, mais c'est un peu un overkill et on ne doit pas changer les fonctions donc tester cela demanderait bcp de travail pour rien.
    # il faut aussi ajouter temporairement une propriété chevalet à Joueur pour avoir accès à l'attribut privé.

    # J'ai testé et tout fonctionne. je commente les tests pour les empêcher de rouler à chaque fois.

    # for jeton in scrabble.tirer_jetons(scrabble.joueur_actif.nb_a_tirer):
    #     scrabble.joueur_actif.ajouter_jeton(jeton)
    #
    # ancien_chevalet = list(scrabble.joueur_actif.chevalet)
    # nbr_jetons_libres = len(scrabble.jetons_libres)
    # scrabble.changer_jetons()
    # assert scrabble.joueur_actif.nb_a_tirer == 0
    # assert scrabble.joueur_actif.chevalet != ancien_chevalet
    # assert len(scrabble.jetons_libres) == nbr_jetons_libres

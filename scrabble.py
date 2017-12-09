import pickle
from random import randint, shuffle
from case import Case
from joueur import Joueur
from jeton import Jeton
from plateau import Plateau
from utils import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import askstring
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

    PADX = 10
    PADY = 10

    def __init__(self):
        super().__init__()

        self.reset_partie()

        # Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(width=800, height=600)

        # Création du menu
        self.barre_menu = Menu(self)
        self.fichier = Menu(self.barre_menu, tearoff=0)
        self.fichier.add_command(label="Nouvelle partie", command=self.nouvelle_partie)
        self.fichier.add_command(label="Sauvegarder la partie", state=DISABLED, command=self.sauvegarder_partie)  # TODO: state active quand une partie est en cours
        self.fichier.add_command(label="Charger une partie", command=self.charger_partie)
        self.fichier.add_separator()
        self.fichier.add_command(label="Quitter", command=self.quit)
        self.barre_menu.add_cascade(label="Fichier", menu=self.fichier)

        self.aide = Menu(self.barre_menu, tearoff=0)
        self.aide.add_command(label="Règlements", state=DISABLED)  # TODO: faire apparaître une fenêtre avec les règlements ->
        self.barre_menu.add_cascade(label="Aide", menu=self.aide)

        self.config(menu=self.barre_menu)

        # On appelle la fenêtre principale et  l'écran d'accueil
        self.config_content()
        self.accueil()

    def reset_partie(self):
        # Declare parameters
        self.liste_langue = ['fr', 'en']
        self.langue='fr'
        self.difficulte = 'facile'
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
        self.affichage_joueur = None

    def config_content(self):
        """
        Configure la fenêtre principale
        :return: Aucun
        """
        self.content = Frame(self)
        self.content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW, padx=5, pady=5)
        self.content.grid_columnconfigure(0, weight=2)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

    def accueil(self):
        """
        Affichage de l'écran d'accueil.
        :return: Aucun
        """
        accueil = Frame(self.content)
        accueil.grid(row=0, column=0, rowspan=2, columnspan=2)

        # message de bienvenue
        Label(accueil, text="Bienvenue dans IFT-1004 Scrabble", font=("Times", 24)).grid(row=0, columnspan=5)
        # label de la langue
        Label(accueil, text="Choisissez la langue du jeu:", font=("Times", 16)).grid(row=1, column=0, sticky=E, padx=self.PADX, pady=self.PADY)

        # Choix des langues
        langue = StringVar()
        langue.set('fr')
        Radiobutton(accueil, text='Français', variable=langue, value='fr').grid(row=1, column=1, sticky=W, pady=self.PADY)
        Radiobutton(accueil, text='English', variable=langue, value='en').grid(row=1, column=2, sticky=W, pady=self.PADY)

        # Nombre des joueurs
        Label(accueil, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=2, column=0, sticky=E, padx=self.PADX, pady=self.PADY)
        nb_joueurs = IntVar()
        nb_joueurs.set(2)
        Radiobutton(accueil, text='2 joueurs', variable=nb_joueurs, value=2).grid(row=2, column=1, sticky=W, pady=self.PADY)
        Radiobutton(accueil, text='3 joueurs', variable=nb_joueurs, value=3).grid(row=2, column=2, sticky=W, pady=self.PADY)
        Radiobutton(accueil, text='4 joueurs', variable=nb_joueurs, value=4).grid(row=2, column=3, sticky=W, pady=self.PADY)
        Radiobutton(accueil, text='Jouer contre l\'ordinateur', variable=nb_joueurs, value=1, state=DISABLED).grid(row=2, column=4, sticky=W, pady=self.PADY)

        # Difficulté
        Label(accueil, text="Choisissez la difficulté:", font=("Times", 16)).grid(row=3, column=0, sticky=E, padx=self.PADX, pady=self.PADY)
        difficulte = StringVar()
        difficulte.set('facile')
        Radiobutton(accueil, text='Facile', variable=difficulte, value='facile').grid(row=3, column=1, sticky=W)
        Radiobutton(accueil, text='Règles officielles', variable=difficulte, value='difficile').grid(row=3, column=2, sticky=W)

        # Débuter la partie
        Button(accueil, text="Commencer une nouvelle partie", command=lambda: self.demarrer_partie(accueil, nb_joueurs.get(), langue.get(), difficulte.get())).grid(row=4, column=1, columnspan=2, sticky=NSEW, pady=self.PADY)
        Button(accueil, text="Charger une partie existante", command=self.charger_partie).grid(row=5, column=1, columnspan=2, sticky=NSEW, pady=self.PADY)

    def nouvelle_partie(self):
        """
        Détruit la partie en cour et retourne à l'accueil
        :return: aucun
        """
        self.content.destroy()
        self.reset_partie()
        self.config_content()
        self.accueil()


    def demarrer_partie(self, accueil, nb_joueurs, langue, difficulte):
        """
        Démarre une partie en détruisant la page d'accueil, initialisant la partie et passe le contrôle à jouer().
        :param accueil: (Frame) Page d'accueil
        :param nb_joueurs: (int) Nombre de joueurs
        :param langue: (str) Code de langue à 2 lettres
        :param difficulte: str, option de difficulté de la partie, 'facile' ou 'difficile'
        :return: aucun return
        """
        accueil.destroy()
        self.initialiser_partie(nb_joueurs, langue, difficulte)
        self.jouer()
        self.changer_joueur()

    def initialiser_partie(self, nb_joueurs, langue, difficulte, joueurs=None):
        """
        - La liste des joueurs est créée et chaque joueur porte automatiquement le nom Joueur 1, Joueur 2, ... Joueur n où n est le nombre de joueurs;
        - Le sac à jetons (self.jetons_libres) est créé
        - Le dictionnaire est ouvert

        :param nb_joueurs: int, nombre de joueurs de la partie au minimun 2 au maximum 4.
        :param langue: str, abbréviation à 2 lettres de la langue
        Dépendamment de la langue, on doit ouvrir, lire, charger en mémoire le bon dictionnaire.
        Les dictionnaires sont dans le dossier dic et sont nommés par l'abbéviation à deux lettres de la langue du dictionnaire.
        Exemple: le chemin d'accès du dictionnaire français est 'dic/fr.txt' et celui du dictionnaire anglais est 'dic/en.txt'
        Ensuite il suffit d'extraire les mots contenus pour construire un set avec le mot clé set.
        Aussi, grâce à la langue vous devez être capable de créer tous les jetons de départ et les mettre dans jetons_libres.

        Pour savoir combien de jetons sont créés pour chaque langue vous pouvez regarder à l'adresse:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble

        :param difficulte: str, difficulté de la partie -> facile et difficile. Le mode difficile implémente les règles officielles du jeu de Scrabble
        :param joueurs: Liste des joueurs, None par défaut. Passé en argument si on charge une partie.
        :exception: Levez une exception avec assert si la langue n'est ni fr ou en ou si nb_joueur < 2 ou > 4.
        """

        assert 2 <= nb_joueurs <= 4
        assert langue.lower() in self.liste_langue
        self.langue = langue.lower()
        self.joueurs = joueurs
        if self.joueurs is None:
            self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]
        print(self.joueurs)

        self.difficulte = difficulte

        if self.jetons_libres is None or self.jetons_libres == []:
            with open('data/{}.txt'.format(self.langue), 'r') as data:
                self.jetons_libres = []
                for line in data.read().splitlines():
                    temp = line.split(',')
                    lettre = str(temp[0])
                    occurences = int(temp[1])
                    valeur = int(temp[2])
                    joker = temp[3]
                    for _ in range(occurences):
                        self.jetons_libres.append(Jeton(lettre, valeur, joker))

        with open('dic/{}.txt'.format(self.langue), 'r') as dic:
            self.dictionnaire = set([x[:-1].upper() for x in dic.readlines() if len(x[:-1]) > 1])

    def jouer(self, cases=None, positions=None, jetons_places=None):
        """
        La fonction démarre une partie de scrabble.
        Pour une nouvelle partie de scrabble,
        - un nouvel objet Plateau est créé;
        - Affiche le pointage
        - Affiche le message du tour en cours
        - Crée le Canvas du chevalet
        - Affiche les boutons d'actions
        :param cases: Liste des cases, None par défaut, passé en argument quand on charge une partie.
        :param positions: tuples list, Liste de positions en forme de tuple (i,j),None par défaut, passé en argument quand on charge une partie.
        :param jetons_places: Liste des jetons placée durant le tour. None par défaut, passé en argument quand on charge une partie.
        """

        # Set le plateau
        self.plateau = Plateau(self.content, self.PIXELS_PAR_CASE, cases, positions, jetons_places)
        self.plateau.grid(row=0, column=0, rowspan=4, columnspan=1, sticky=NSEW)

        # Set le tableau d'affichange
        self.tableau = Frame(self.content)
        self.tableau.grid(row=0, column=1, columnspan=3, sticky=NSEW)
        Label(self.tableau, textvariable=self.message).grid(row=0, columnspan=2)
        Label(self.tableau, textvariable=self.pointage).grid(row=1, columnspan=2)

        # Timer (version difficile uniquement)
        if self.difficulte == 'difficile':
            Label(self.tableau, text='Temps restant au tour: ').grid(row=3, column=0, pady=self.PADY)
            self.timer_label = Label(self.tableau, text='')
            self.timer_label.grid(row=3, column=1, pady=self.PADY)
            self.set_clock()
            self.clock()

        # Set les joueurs
        self.affichage_joueur = Frame(self.content)
        self.affichage_joueur.grid(row=1, column=1, rowspan=1, columnspan=3, sticky=NSEW)
        Label(self.affichage_joueur, textvariable=self.nom_joueur).grid(row=0, column=0, columnspan=3)
        self.chevalet_actif = Canvas(self.affichage_joueur, height=self.PIXELS_PAR_CASE, width=self.PIXELS_PAR_CASE*Joueur.TAILLE_CHEVALET, bg='#f5ebdc')
        self.chevalet_actif.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Set les boutons d'actions
        btn_jouer = Button(self.affichage_joueur, text="Joueur le tour", command=self.jouer_un_tour)
        btn_annuler = Button(self.affichage_joueur, text="Annuler", command=self.reprendre_tous_les_jetons)
        btn_passer = Button(self.affichage_joueur, text="Passer le tour", command=self.passer_un_tour)
        btn_changer = Button(self.affichage_joueur, text="Changer les jetons", command=self.demander_jetons_a_changer)
        btn_quitter = Button(self.affichage_joueur, text="Quitter la partie", command=self.quitter)

        # Affichage des boutons d'actions
        btn_jouer.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=30)
        btn_annuler.grid(row=2, column=2, columnspan=2, sticky=NSEW, pady=30)
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
            dessiner_jeton(self.plateau, x1, y1, x2, y2, delta, self.joueur_actif.jeton_actif, ('jeton','jeton_place', "jeton_{}_{}".format(ligne, col)))

            self.joueur_actif.jeton_actif = None

            self.unbind_redeposer()
            self.unbind_poser()
            self.after(500, self.bind_reprendre)
        except (CaseOccupeeException, AssertionError) as e:
            showwarning(message=e)
            print(e) # TODO: améliorer la gestion des erreurs!

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
        if self.joueur_actif.jeton_actif is not None:
            try:
                pos = self.joueur_actif.chevalet.index(None)
                self.joueur_actif.ajouter_jeton(self.joueur_actif.jeton_actif, pos)

                x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)

                dessiner_jeton(self.chevalet_actif, x1, y1, x2, y2, delta,self.joueur_actif.jeton_actif, ('chevalet', 'chevalet{}'.format(pos)))
                self.joueur_actif.jeton_actif = None

                self.unbind_redeposer()
                self.unbind_poser()
            except PositionChevaletException as e:
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
                self.bind_poser()
            except (PositionChevaletException, AssertionError) as e:
                print(e)

    def jeter_jeton(self, event):
        """
        Permet de retirer un jeton du chevalet du joueur et le placer dans le chevalet des jetons à jeter.
        :param event: Le clic de souris ayant déclenché l'évènement
        :return: aucun
        """
        pos = floor(event.x / self.PIXELS_PAR_CASE)

        nb_jetons = len(self.joueur_actif.chevalet)
        jeton_retire = self.joueur_actif.retirer_jeton(pos)

        # assert len(self.joueur_actif.chevalet) < nb_jetons
        # TODO: régler le bug qui fait que les jetons ne se retirent pas bien du chevalet.

        self.joueur_actif.jetons_jetes.append(jeton_retire)

        x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)
        dessiner_jeton(self.sac_a_jetons, x1, y1, x2, y2, delta, jeton_retire, 'chevalet{}'.format(pos))
        self.chevalet_actif.delete('chevalet{}'.format(pos))

    def reprendre_jeton(self, event):
        """
        Permet de reprendre un jeton déposé sur le plateau par le joueur.
        - Vérifier que le jeton a été placé lors du tour courant
        - Vérifier que le joueur n'est pas en train de poser un jeton (il n'y a pas de jeton_actif)
        - Retirer le jeton de la case
        - Effacer le jeton du plateau
        - Enlever la case et le jeton des listes cases_placees et jetons_places
        - Binder redéposer
        """
        ligne, col, case = self.determiner_case(event)

        # Vérifie que le jeton a bien été placé dans le tour courant
        if (ligne, col) not in self.plateau.positions:
            return

        # Reprend le jeton
        if self.joueur_actif.jeton_actif is None:
            # Todo: vérifier -> le try/except est pas vrmt utile ici je crois, car le cases vides ne sont même pas bindées à la souris...
            # donc aucun moyen d'arriver ici à partir d'une case vide...
            try:
                jeton = case.retirer_jeton()
                self.plateau.delete("jeton_{}_{}".format(ligne, col))

                self.plateau.jetons_places.remove(jeton)
                self.joueur_actif.jeton_actif = jeton
                self.plateau.positions.remove((ligne, col))

                self.bind_redeposer()
                self.bind_poser()
            except CaseVideException as e:
                print(e)


    def jouer_un_tour(self):
        """
        Permet à un joueur de jouer un tour. La fonction vérifie que les mots placés sont acceptés et met à jour les scores.
        Si les mots sont corrects, on change de joueur, sinon on avertit quels mots ne sont pas permis et le joueur peut continuer à jouer son tour.
        - Vérifier la validité des positions des cases
        - Calculer les mots et le score obtenus et vérifier si tous les mots sont permis
        - Ajouter les points au joueur
        - Resetter les listes de positions et jetons placés
        - changer de joueur
        :return: Aucun return
        """
        #Vérifie si le joueur a placé des jetons
        if len(self.plateau.positions) == 0 or len(self.plateau.jetons_places) == 0:
            showinfo(message="Vous n'avez pas placé de jetons!\nSi vous ne désirez pas jouer ce tour-ci, "
                                           "veuillez sélectionner le bouton 'Passer le tour'")
            return

        # Vérifie la validité des positions des jetons placés
        try:
            self.plateau.valider_positions(self.plateau.positions)
        except (CasesNonEnLigneException, PasDeCasesAdjacentes, CaseVideDansMot, CentreNonUtilise) as e:
            showwarning(message=e)
            return

        # Vérifier la présence d'un joker
        try:
            jokers = [jeton.est_un_joker() for jeton in self.plateau.jetons_places]
            if any(jokers):
                for jeton in range(jokers.count(True)):
                    lettre = askstring('Joker', "Entrez la lettre que vous souhaitez attribuer au joker.\nSi vous avez mis plusieurs jokers, "
                                                "entrez les lettres dans l'ordre que vous les avez placés.")
                    if len(lettre) != 1 or not lettre.isalpha():
                        raise LettreInvalideException("La lettre entrée n'est pas valide.")

                    # On trouve l'index du premier joker
                    index_joker = jokers.index(True)
                    # On met false à ce joker pour éviter qu'il soit repris si on a plusieurs jokers
                    jokers[index_joker] = False
                    # On change la lettre du jeton pour la lettre entrée. Pour le reste de la partie, ce jeton sera cette lettre
                    self.plateau.jetons_places[index_joker].lettre = lettre.upper()

        except LettreInvalideException as e:
            showwarning(message=e)
            return

        # Vérifie si les mots sont permis
        try:
            mots, score = self.plateau.mots_score_obtenus(self.plateau.positions)
            mots_non_permis = [mot for mot in mots if not self.mot_permis(mot)]

            # Si un mot non permis est présent
            if len(mots_non_permis) != 0:
                msg = "Un ou plusieurs mots ne sont pas permis:\n"
                for mot in mots_non_permis:
                    msg = msg + "- " + mot + "\n"
                # pour la version facile, on notifie le joueur des mots non permis et il peut continuer son tour
                if self.difficulte == 'facile':
                    raise MotNonPermisException(msg)
                # pour la version officielle (difficile), on reprend tous les jetons et le joueur passe son tour
                else:
                    self.reprendre_tous_les_jetons()
                    self.passer_un_tour()
                    raise MotNonPermisException(msg)

            # Si toutes les lettres sont placés, on ajoute 50 points, car c'est un Scrabble!
            if len(self.plateau.jetons_places) == Joueur.TAILLE_CHEVALET:
                showinfo('Scrabble!', 'Félicitations! Vous avez placé tous vos jetons!\nVous obtenez 50 points boni!')
                score += 50
        except MotNonPermisException as e:
            showwarning(message=e)
            return

        self.joueur_actif.ajouter_points(score)
        self.plateau.positions = []
        self.plateau.jetons_places = []
        self.changer_joueur()

    def reprendre_tous_les_jetons(self):
        """
        - retirer les jetons du plateau et effacer la représentation graphique des jetons
        - ajouter les jetons au chevalet du joueur et dessiner les jetons sur le chevalet
        - vérifier s'il y a un jeton actif et le replacer aussi
        - "vider" jeton_actif, positions et jetons placés et binder prendre un jeton
        :return: aucun
        """
        if len(self.plateau.positions) > 0:
            for (ligne, col) in self.plateau.positions:
                # Retirer le jeton du plateau
                jeton_retire = self.plateau.cases[ligne][col].retirer_jeton()
                self.plateau.delete("jeton_{}_{}".format(ligne, col))
                # Ajouter le jeton au chevalet
                pos = self.joueur_actif.chevalet.index(None)
                self.joueur_actif.ajouter_jeton(jeton_retire, pos)
                x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)
                dessiner_jeton(self.chevalet_actif, x1, y1, x2, y2, delta, jeton_retire, ('chevalet', 'chevalet{}'.format(pos)))

        # Ajouter le jeton actif au chevalet
        if self.joueur_actif.jeton_actif is not None:
            pos = self.joueur_actif.chevalet.index(None)
            self.joueur_actif.ajouter_jeton(self.joueur_actif.jeton_actif, pos)
            x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)
            dessiner_jeton(self.chevalet_actif, x1, y1, x2, y2, delta, self.joueur_actif.jeton_actif, ('chevalet', 'chevalet{}'.format(pos)))
            self.joueur_actif.jeton_actif = None

        # réinitialiser les valeurs
        self.plateau.positions = []
        self.plateau.jetons_places = []
        self.bind_prendre()

    def passer_un_tour(self):
        """
        Permet à un joueur de passer son tour.
        - vérifier que le joueur n'a pas placé de jetons sur le plateau
        - changer de joueur
        :return: aucun retour
        """
        # Vérifie si le joueur a placé des jetons
        if len(self.plateau.positions) != 0 or len(self.plateau.jetons_places) != 0:
            showinfo(message="Vous avez placé de jetons!\nSi vous désirez passer votre tour, "
                                        "retirez vos jetons du plateau.\n"
                                        "Sinon, sélectionnez 'Jouer un tour'")
            return

        self.changer_joueur()

    def quitter(self):
        """
        Retire un joueur de la liste des joueurs
        :return: Aucun return
        """
        # Vérifie si le joueur a placé des jetons
        if len(self.plateau.positions) != 0 or len(self.plateau.jetons_places) != 0:
            showinfo(message="Vous avez placé de jetons!\nSi vous désirez abandonner, "
                                        "retirez vos jetons du plateau.\n"
                                        "Sinon, sélectionnez 'Jouer un tour'")
            return

        quitter = self.joueur_actif
        self.changer_joueur()
        self.joueurs.remove(quitter)

        # Vérifie si la partie est terminée
        if self.partie_terminee():
            showinfo('Partie terminée', '{} est le gagnant! Félicitations!'.format(self.determiner_gagnant().nom))
            return

    def demander_jetons_a_changer(self):
        """
        Interface graphique pour changer les jetons
        - unbinder la fonction prendre
        - afficher le sac a jeton et les boutons
        - binder la fonction jeter
        :return: Aucun return
        :exception: Lever une exception si le nombre de jetons à changer est supérieur au nombre de jetons restants.
        """
        # Vérifie si le joueur a placé des jetons
        if len(self.plateau.positions) != 0 or len(self.plateau.jetons_places) != 0:
            showinfo(message="Vous avez placé de jetons!\nSi vous désirez changer des jetons, "
                                        "retirez vos jetons du plateau.\n"
                                        "Sinon, sélectionnez 'Jouer un tour'")
            return

        # Bindings
        self.unbind_prendre()
        self.bind_jeter()

        # Affichage de l'interface
        self.bottom_right = Frame(self.content)
        self.bottom_right.grid(row=2, column=1, rowspan=1, columnspan=3, sticky=NSEW)
        Label(self.bottom_right, text="Sélectionner les jetons à changer\net appuyez sur Confirmer").grid(row=0, column=0, columnspan=2)
        self.sac_a_jetons = Canvas(self.bottom_right, width=self.PIXELS_PAR_CASE*Joueur.TAILLE_CHEVALET, height=self.PIXELS_PAR_CASE, bg="#f5ebdc")
        self.sac_a_jetons.grid(row=1, column=0, columnspan=2)
        Button(self.bottom_right, text="Confirmer", command=self.changer_jetons).grid(row=3, column=0)
        Button(self.bottom_right, text="Cancel", command=self.annuler_changer_jetons).grid(row=3, column=1)

    def changer_jetons(self):
        """
        Change les jetons sélectionnés par le joueur.
        - On tire de nouveaux jetons dans le sac à jetons
        - On ajoute les jetons tirés au chevalet du joueur
        - On retourne les jetons jetés par le joueur dans le sac à jetons
        - unbind jeter_jeton et rebind prendre jeton
        - effacer le frame pour changer les jetons
        - On passe au joueur suivant
        :return: Aucun return
        """
        # Piger de nouveaux jetons et retourner les jetons jetés au sac à jetons
        jetons_a_ajouter = self.tirer_jetons(self.joueur_actif.nb_a_tirer)
        for jeton in jetons_a_ajouter:
            self.joueur_actif.ajouter_jeton(jeton)
        self.jetons_libres = self.jetons_libres + self.joueur_actif.jetons_jetes

        # Détruire l'interface pour changer les jetons
        self.unbind_jeter()
        self.bind_prendre()
        self.bottom_right.destroy()
        # Passer un tour
        self.changer_joueur()

    def annuler_changer_jetons(self):
        """
        - Remettre les jetons dans le chevalet du joueur.
        - unbind jeter_jeton et rebind prendre_jeton
        - effacer le frame pour changer les jetons
        :return:
        """
        # Remettre les jetons jetés dans le chevalet du joueur
        for jeton in self.joueur_actif.jetons_jetes:
            self.joueur_actif.ajouter_jeton(jeton)
        self.dessiner_chevalet(self.chevalet_actif,self.joueur_actif)
        self.joueur_actif.jetons_jetes = []
        # Détruire l'interface pour changer les jetons
        self.unbind_jeter()
        self.bind_prendre()
        self.bottom_right.destroy()

    def changer_joueur(self, charger=False, tour=0):
        """
        Change le joueur. C'est l'action de passer le tour au prochain joueur. La méthode change le joueur actif et affiche dans l'interface les infos du nouveau joueur.
        La méthode vérifie aussi si la partie est terminée.
        :param charger: Bool, False par défaut, True quand une partie est chargée
        :param tour ; int, 0 par défaut, si on charge une partie le tour sera affecté
        :return: Aucun return
        """

        # Vérification si la partie est terminée
        if self.partie_terminee():
            showinfo('Partie terminée', '{} est le gagnant! Félicitations!'.format(self.determiner_gagnant().nom))
            return
            # TODO: vérifier pour cette condition si l'exécution se fait bien et potentiellement améliorer l'action

        # On passe au joueur suivant et on incrémente le tour de la partie, si on ne charge pas une partie
        if charger is False:
            self.joueur_suivant()
        if tour == 0:
            self.plateau.tour += 1
        else:
            self.plateau.tour = tour

        # On détermine le message à afficher
        if self.plateau.tour == 1:
            msg = "Tour {}\nLa partie va commencer avec le {}".format(self.plateau.tour, self.joueur_actif.nom)
        else:
            msg = "Tour {}\nC'est le tour de {}".format(self.plateau.tour, self.joueur_actif.nom)

        # On pige les jetons
        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)

        # On update l'affichage
        self.message.set(msg)
        self.pointage.set(self.msg_points())
        self.nom_joueur.set(self.joueur_actif.nom)
        self.dessiner_chevalet(self.chevalet_actif, self.joueur_actif)
        self.bind_prendre()

        if self.difficulte == "difficile":
            self.set_clock()

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
        #todo: à voir si on peut améliorer ce qui se passe quand une partie termine

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

    def set_clock(self):
        """
        Fonction utilitaire simple qui reset le timer au temps permis (difficulté 'difficile' utilisant les règles officielles)
        :return: Aucun
        """
        self.timer = 60

    def clock(self):
        """
        Fonction responsable de faire fonctionner le timer pour limiter le temps alloué par tour dans la difficulté 'difficile' officielle.
        Est aussi responsable de l'affichage du timer dans l'interface
        :return: Aucun
        """
        self.timer -= 1
        if self.timer == 0:
            self.temps_ecoule()
        self.timer_label['text'] = self.timer
        self.timer_label.after(1000, self.clock)

    def temps_ecoule(self):
        """
        Fonction appelée lorsque le temps par tour alloué est écoulé dans la version 'difficile' utilisant les règles officielles.
        Reprend tous les jetons placés et les retourne dans le chevalet du joueur avant de changer de joueur.
        :return: Aucun
        """
        showwarning('Temps écoulé', 'Vous avez épuisé tout le temps permis!\nVous passez votre tour.')
        self.reprendre_tous_les_jetons()
        self.changer_joueur()

    def bind_poser(self):
        """
        Fonction utilitaire pour binder le clic de souris à la pose d'un jeton sur une case
        """
        self.plateau.tag_bind('case', '<Button-1>', self.poser_jeton)

    def unbind_poser(self):
        """
        Fonction utilitaire pour unbinder le clic de souris à la pose d'un jeton sur une case
        """
        self.plateau.tag_bind('case', '<Button-1>', lambda e: "break")

    def bind_prendre(self):
        self.chevalet_actif.tag_bind('chevalet', '<Button-1>', self.prendre_jeton)

    def unbind_prendre(self):
        self.chevalet_actif.tag_bind('chevalet', '<Button-1>', lambda e: "break")

    def bind_jeter(self):
        self.chevalet_actif.tag_bind('chevalet', '<Button-1>', self.jeter_jeton)

    def unbind_jeter(self):
        self.chevalet_actif.tag_bind('chevalet', '<Button-1>', lambda e: "break")

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

    def sauvegarder_partie(self):
        """
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :return: Aucun
        """

        # Note: ici la stratégie est de dumper les infos qui sont propres à la partie
        # self.langue
        # self.joueur_actif
        # self.joueurs
        # self.jetons_libres
        # self.plateau.cases
        # self.plateau.tour
        # self.plateau.positions
        # self.plateau.jetons_places

        # Ok j'ai trouvé le moyen le plus simple d'avoir une boite de dialogue pour entrer le nom de fichier c'est dans
        # le module simpledialog. Plus besoin de demander_sauvegarder_partie
        nom_fichier = askstring("Sauvegarder", "Entrez le nom de la sauvegarde:")

        try:
            with open(nom_fichier, "wb") as f:
                print("DÉBUT SAUVEGARDE")

                pickle.dump(self.langue, f)
                print(self.langue)

                pickle.dump(self.joueurs, f)
                print(self.joueurs)

                for positions in range(len(self.joueurs)):
                    if self.joueurs[positions] == self.joueur_actif:
                        position_joueur_actif = positions
                        print(position_joueur_actif)
                pickle.dump(position_joueur_actif, f)

                pickle.dump(self.jetons_libres, f)
                print(self.jetons_libres)

                pickle.dump(self.plateau.cases, f)
                print(self.plateau.cases)

                pickle.dump(self.plateau.tour, f)
                print(self.plateau.tour)

                pickle.dump(self.plateau.positions, f)
                print(self.plateau.positions)

                pickle.dump(self.plateau.jetons_places, f)
                print(self.plateau.jetons_places)

                pickle.dump(self.difficulte, f)
                print(self.difficulte)

        except:
            print("echec de la sauvegarde")
            return False

    def charger_partie(self):
        """
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment.
        :return:
        """
        nom_fichier = askstring("Charger une partie", "Entrez le nom du fichier à charger:")

        with open(nom_fichier, "rb") as f:
            try:
                print("DÉBUT LOAD")

                langue = pickle.load(f)
                print(langue)

                joueurs = pickle.load(f)
                print(joueurs,"JOUEURS CHARGÉS")
                print(joueurs[1].points)

                position_joueur_actif = pickle.load(f)
                print(position_joueur_actif)

                jetons_libres = pickle.load(f)
                print(jetons_libres)

                cases = pickle.load(f)
                print(cases)

                tour = pickle.load(f)
                print(tour)

                positions = pickle.load(f)
                print(positions)

                jetons_places = pickle.load(f)
                print(jetons_places)

                difficulte = pickle.load(f)
                print(difficulte)

                assert cases is not None # ça c'est pas forcément utile... c'est trop général utilises plutôt :
                assert isinstance(cases, list)
                assert all([isinstance(case, Case) for ligne in cases for case in ligne])
                assert isinstance(position_joueur_actif, int)

            # ici tu peux en mettre plusieurs en t'inspirant de ceux que j'ai mis pour vérifier que les données sont bonnes.

            except AssertionError as e:
                print(e)
                return

        # Une fois que tu as vérifié que les données sont bonnes, tu peux sortir de la boucle 'with open' en désindentant comme j'ai fait ici
        # ça va fermer le fichier car tu n'en a plus besoin.

        # self.demarrer_partie(self, nb_joueurs=len(joueurs), langue=self.langue, difficulte=self.difficulte)
        # ici il est sans doute mieux d'utiliser la fonction initialiser_partie()
        # demarrer partie est pour aussi détruire l'accueil. ici on ne passe pas par l'accueil... donc ça va bugger pcq il va essayer de détruire qqc qui n'existe pas.

        # Aussi, même si tu voulais utiliser la fonction demarrer_partie, les arguments qu'il faut que tu passes sont ACCUEIL, nb_joueurs, etc. -> self = Scrabble dans ce cas-ci
        # Forcément ça va bugger! en appelant la fonction démarrer_partie comme tu le fais, ce que tu te retrouves à faire c'est détruire Scrabble pcq tu passes self
        # à la place de l'accueil donc il détruit self -> donc il s'autodétruit.... haha

        # rappelle toi aussi qu'écrire self.fonction() c'est juste un raccourci pour écrire Class.fonction(self), donc si tu appelles une fonction en écrivant
        # self.fonction() tu lui passes self en 1er argument de façon implicite. donc c'est bien rare que tu vas écrire self.fonction(self) à moins d'un cas particulier.

        # Ici je t'ai fait un petit plan de comment faire. Je ne peux pas tester, donc c'est sûr que ça marchera probablement pas du 1er coup.
        # mais je voulais juste te donner une base...

        # on détruit la fenêtre principale et on la recrée pour être sûr qu'elle est "propre"
        self.content.destroy()
        self.config_content()

        #set param
        self.joueur_actif = joueurs[position_joueur_actif]
        assert self.joueur_actif in joueurs
        self.jetons_libres = jetons_libres
        print(self.jetons_libres)
        # On initialise la partie
        self.initialiser_partie(len(joueurs), langue, difficulte, joueurs=joueurs)

        # On set les paramètres
        #self.joueur_actif = joueur_actif
        #self.jetons_libres = jetons_libres
        #self.plateau.cases = cases
        #self.plateau.tour = tour
        #self.plateau.positions = positions
        #self.plateau.jetons_places = jetons_places

        # OK! J'ai compris une partie du problème. Les ids des objets changent on dirait -> regarde le chiffre à côté de object at 0x10390.... entre un save et un load, ça change
        # d'où l'erreur quand il essaie de changer de joueur par exemple.
        # peut-être que ça serait mieux de saver le nom ou l'index du joueur actif.. qqc comme ça.
        # bon je t'ai donné quelques pistes, mais c'est juste des idées, continues la-dessus
        # je pensais t'avoir donner une partie facile... erreur. lol

        # On lance la partie
        self.jouer(cases, positions)

        self.changer_joueur(charger=True, tour=tour)
        # j'ai ajouté un paramètre pour ne pas faire changer de joueur quand on charge une partie, ainsi que tour

    # def demande_sauvegarder_partie(self):

        # Commentaire: ici on peut utiliser la méthode simple et juste y aller avec ta 1ere méthode
        # sinon on peut y aller avec la méthode compliquée et utiliser sys.platform du module sys pour déterminer l'OS et proposer la bonne méthode à chaque.

        # self.nom_fichier = filedialog.asksaveasfilename(initialdir="/", title="Sélectionnez un fichier", filetypes=(("all files", "*.*"),))
        # print(self.nom_fichier)
        #
        # self.sauvegarder_partie(self.nom_fichier)

        # self.fenetre_sauv = Toplevel(self)
        # self.fenetre_sauv.title("Sauvegarder")
        # cadre_label_entry = Frame(self.fenetre_sauv, padx=10, pady=10)
        # cadre_label_entry.grid(row=0)
        #
        # label_sauvegarde = Label(cadre_label_entry, text="Entrez le nom de la sauvegarde:", padx=10, pady=10)
        # label_sauvegarde.grid(row=0)
        #
        # nom_fichier =StringVar()
        #
        # entry_sauvegarde = Entry(cadre_label_entry, textvariable=nom_fichier)
        # entry_sauvegarde.grid(row=1)
        #
        # cadre_btn = Frame(self.fenetre_sauv, padx=10, pady=10)
        # cadre_btn.grid(row=1)
        # btn_ok = Button(cadre_btn, text="Sauvegarder", padx=10, pady=10,
        #                 command=lambda: self.sauvegarder_partie(nom_fichier.get()))
        # btn_ok.grid(row=0, column=0)
        # btn_cancel = Button(cadre_btn, text="Annuler",  padx=10, pady=10, command=self.fenetre_sauv.destroy)
        # btn_cancel.grid(row=0, column=2)



    # def demander_charger_partie(self):
    #
    #     # self.nom_fichier = filedialog.askopenfilename(initialdir="C:/PROJET_PYTHON/tp4", title="Sélectionnez un fichier",
    #     #                                               filetypes=(("all files", "*.*"),))
    #     # print(self.nom_fichier)
    #     # self.charger_partie(self.nom_fichier)
    #
    #     self.fenetre_charger = Toplevel(self)
    #     self.fenetre_charger.title("Charger une partie")
    #     cadre_label_entry = Frame(self.fenetre_charger, padx=10, pady=10)
    #     cadre_label_entry.grid(row=0)
    #
    #     label_sauvegarde = Label(cadre_label_entry, text="Entrez le nom de la partie à charger:", padx=10, pady=10)
    #     label_sauvegarde.grid(row=0)
    #
    #     nom_fichier = StringVar()
    #
    #     entry_sauvegarde = Entry(cadre_label_entry, textvariable=nom_fichier)
    #     entry_sauvegarde.grid(row=1)
    #
    #     cadre_btn = Frame(self.fenetre_charger, padx=10, pady=10)
    #     cadre_btn.grid(row=1)
    #     btn_ok = Button(cadre_btn, text="Charger", padx=10, pady=10,
    #                     command=lambda: self.charger_partie(nom_fichier.get()))
    #     btn_ok.grid(row=0, column=0)
    #     btn_cancel = Button(cadre_btn, text="Annuler", padx=10, pady=10, command=self.fenetre_charger.destroy)
    #     btn_cancel.grid(row=0, column=2)


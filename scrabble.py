import pickle
import inspect
from random import randint, shuffle
from tkinter.messagebox import *
from tkinter.simpledialog import askstring
from tkinter.filedialog import *
from exception import *
from case import Case
from joueur import Joueur
from plateau import Plateau
from reglements import Reglements
from utils import *
from accueil import Accueil
from jeu import Jeu


class Scrabble(Tk):
    """
    Classe Scrabble qui implémente aussi une partie de la logique de jeu.

    Les interfaces:
        - content: tk.Frame, Frame conteneur principale. Parent de tous les autres frames.
        - accueil: Accueil(tk.Frame), objet de la classe Accueil héritant de tk.Frame. C'est l'écran d'accueil avec les options
        - jeu: Jeu(tk.Frame), objet de la classe Jeu héritant de tk.Frame. C'est l'écran de jeu principal.

    Les attributs couramment utilisés d'un scrabble sont:
        - plateau: Plateau(tk.Canvas), un objet de la classe Plateau héritant de tk.Canvas on y place des jetons et il nous dit le nombre de points gagnés.
        - jetons_libres: Jeton list, la liste de tous les jetons dans le sac à jetons, c'est là que chaque joueur peut prendre des jetons quand il en a besoin.
        - joueurs: Joueur list,  L'ensemble des joueurs de la partie.
        - joueur_actif: Joueur, le joueur qui est entrain de jouer le tour en cours. Si aucun joueur alors None.
        - langue: str, Abbréviation en 2 lettres de la langue utilisée
        - difficulté: str, Difficulté utilisée dans la parte
        - lettres_def: dict, Dictionnaire des lettres et de leur valeur en points. key:lettre, value:valeur
        - dictionnaire: set, contient tous les mots qui peuvent être joués sur dans cette partie.
        - chevalet_actif: Chevalet(tk.Canvas), un objet de la classe Chevalet héritant de tk.Canvas. Représente le chevalet du joueur actif représenté graphiquement.
        - tour: int, Le numéro du tour en cours. Un tour représente le jeu d'un joueur et non de tous les joueurs.
        - save: str, Chemin d'accès de la sauvegarde courante. Permet de sauvegarder sans entrer le chemin d'accès à chaque fois.

    Les autres attributs:
        - suggestions: tk.Text, Bloc de texte affiché dans le frame suggestions. Suggère des mots possibles au joueur.
        - log: tk.Text, Bloc de texte affiché dans le frame log. C'est l'historique des tours.
                        Contient le tour, l'action du joueur, les mots placés, les points récoltés et le temps du tour.
        - barre_menu: tk.Menu, Barre des menus
        - fichiers: tk.Menu, Le menu "fichiers" de la barre de menus
        - presentation: tk.Menu, Le menu "présentation" de la barre de menus
        - aide: tk.Menu, Le menu "aide" de la barre de menus
        - assist: tk.Frame, Le frame contenant les suggestions. Peut être affiché ou caché via le menu
        - affichage_suggestions: bool, True pour afficher les suggestions, False pour les cacher.
        - message: tk.StringVar, Message dynamique à afficher dans le frame "message" de l'interface.
        - nom_joueur: tk.StringVar, Variable dynamique permettant d'afficher le nom du joueur actif dans l'interface graphique
        - labels_points: tk.Label list, Liste des labels de pointage. Utilisé pour afficher dynamiquement les pointages des joueurs dans l'interface.
        - temps_label: tk.Label, Label du temps écoulé pendant le tour. Utilisé pour afficher dynamiquement l'horloge
        - timer_label: tk.Label, Label du minuteur du temps restant dans le tour. Utilisé pour afficher dynamiquement le minuteur dans la version "difficile".
        - sac_a_jetons_label: tk.Label, Label du Nombre de jetons restants dans les jetons libres (aussi appelé parfois sac à jetons)
        - jobs: dict, Dictionnaire des jobs pour garder la trace des fonctions qui s'appellent elle-mêmes à un intervalle fixe.
                    Possède normalement 2 clés: 'clock' pour l'horloge normale et 'timer' pour le minuteur. La valeur est l'id de la job
                    retourné par la fonction 'after' de clock et tick.
    """
    PIXELS_PAR_CASE = 40
    LANGUES_DISPONIBLES = ['fr', 'en']
    DIFFICULTES_DISPONIBLES = ['facile', 'difficile']
    TAILLE_CHEVALET = 7
    # todo: refactorer -> bouger taille_chevalet et pixels par case

    PADX = 10
    PADY = 10

    def __init__(self):
        super().__init__()

        # Set les variables d'instance
        self.title("PyScrabble")
        self.filename = inspect.getframeinfo(inspect.currentframe()).filename
        self.path = os.path.dirname(os.path.abspath(self.filename))
        self.reset_partie()

        # Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(width=800, height=600)

        # Création du menu
        self.barre_menu = Menu(self)

        # Menu Fichier
        self.fichier = Menu(self.barre_menu, tearoff=0)

        self.fichier.add_command(label="Nouvelle partie", command=self.nouvelle_partie)
        self.fichier.add_command(label="Sauvegarder la partie", command=lambda: self.sauvegarder_partie(nouvelle_sauvegarde=False))
        self.fichier.add_command(label="Enregistrer sous", command=self.sauvegarder_partie)
        self.fichier.add_command(label="Charger une partie", command=self.charger_partie)
        self.fichier.add_separator()
        self.fichier.add_command(label="Quitter", command=self.quitter)

        # Menu Présentation
        self.presentation = Menu(self.barre_menu, tearoff=0)

        self.presentation.add_command(label="Afficher/cacher les suggestions de mots", command=self.toggle_suggestions)
        self.presentation.add_command(label="Afficher/cacher l'historique des tours", command=self.toggle_log)

        # Menu Aide
        self.aide = Menu(self.barre_menu, tearoff=0)
        self.aide.add_command(label="Règlements", command=lambda: Reglements(self))

        # Config du menu
        self.barre_menu.add_cascade(label="Fichier", menu=self.fichier)
        self.barre_menu.add_cascade(label="Présentation", menu=self.presentation)
        self.barre_menu.add_cascade(label="Aide", menu=self.aide)

        self.config(menu=self.barre_menu)

        # On appelle la fenêtre principale
        self.config_content()
        self.show_accueil()

    def reset_partie(self):
        """
        Set les variables d'instance à leur valeur initiales par défaut.
        """
        self.langue = None
        self.difficulte = None
        self.save = None
        self.plateau = None
        self.joueur_actif = None
        self.joueurs = []
        self.jetons_libres = []
        self.lettres_def = {}
        self.dictionnaire = None
        self.message = StringVar()
        self.nom_joueur = StringVar()
        self.chevalet_actif = None
        self.tour = 0
        self.temps = 0
        self.timer = None
        self.suggestions = None
        self.log = None
        self.labels_points = []
        self.timer_label = None
        self.temps_label = None
        self.sac_a_jetons_label = None
        self.jobs = {'clock': None, 'timer': None}
        self.content = None
        self.accueil = None
        self.jeu = None
        self.affichage_suggestions = True
        self.assist = None
        self.affichage_log = True
        self.log_frame = None

    def config_content(self):
        """
        Configure la fenêtre principale. Consiste en un Frame qui contient tous les autres éléments.
        :return: Aucun
        """
        self.content = Frame(self)
        self.content.grid(row=0, column=0, sticky=NSEW)
        self.content.grid_columnconfigure(0, weight=2)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_rowconfigure(2, weight=1)
        self.content.grid_rowconfigure(3, weight=1)
        self.content.grid_rowconfigure(4, weight=1)

    def show_accueil(self):
        """
        Affichage de l'écran d'accueil.
        :return: Aucun
        """
        # Désactive les options nouvelle partie et sauvegarder partie du menu
        self.fichier.entryconfig(0, state="disabled")
        self.fichier.entryconfig(1, state="disabled")
        self.fichier.entryconfig(2, state="disabled")

        self.presentation.entryconfig(0, state="disabled")
        self.presentation.entryconfig(1, state="disabled")

        self.accueil = Accueil(self.content, self)

    def nouvelle_partie(self):
        """
        Détruit la partie en cours et retourne à l'accueil
        :return: aucun
        """
        self.verifier_avant_de_quitter()
        self.content.destroy()
        self.reset_partie()
        self.config_content()
        self.show_accueil()

    def toggle_suggestions(self):
        """
        Permet d'afficher ou de cacher les suggestions de mots pour le joueur.
        """
        if self.affichage_suggestions:
            self.assist.grid_remove()
            self.affichage_suggestions = False
        else:
            self.assist.grid()
            self.affichage_suggestions = True

    def toggle_log(self):
        """
        Permet d'afficher ou de cacher l'historique des tours.
        """
        if self.affichage_log:
            self.log_frame.grid_remove()
            self.affichage_log = False
        else:
            self.log_frame.grid()
            self.affichage_log = True

    def verifier_avant_de_quitter(self):
        """
        Fonction qui demande au joueur s'il veut sauvegarder la partie avant de quitter. Appelée lors de l'utilisation
        des commandes Quitter, Charger une partie et Nouvelle partie
        :return aucun
        """
        if self.plateau is not None and not self.plateau.est_vide():
            sauvegarder = askyesno('Attention', "Voulez-vous sauvegarder la partie en cours avant de quitter?")
            if sauvegarder:
                self.sauvegarder_partie()
            else:
                return

    def quitter(self):
        """
        Fonction qui permet de quitter le jeu de Scrabble de façon sécuritaire en demandant à l'utilisateur s'il souhaite
        sauvegarder la partie courante avant de quitter.
        """
        self.verifier_avant_de_quitter()
        self.quit()

    def demarrer_partie(self, nb_joueurs, langue, difficulte):
        """
        Démarre une partie en détruisant la page d'accueil, initialisant la partie et passe le contrôle à jouer().
        :param nb_joueurs: (int) Nombre de joueurs
        :param langue: (str) Code de langue à 2 lettres
        :param difficulte: str, option de difficulté de la partie, 'facile' ou 'difficile'
        :return: aucun return
        """
        self.initialiser_partie(nb_joueurs, langue, difficulte)
        self.jouer()
        self.changer_joueur()
        self.accueil.grid_remove()

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
        assert langue.lower() in Scrabble.LANGUES_DISPONIBLES
        self.langue = langue.lower()

        if joueurs is None:
            self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]
        else:
            self.joueurs = joueurs

        self.difficulte = difficulte

        if self.jetons_libres is None or self.jetons_libres == []:
            with open('data/{}.txt'.format(self.langue), 'r') as data:
                for line in data.read().splitlines():
                    temp = line.split(',')
                    lettre = str(temp[0])
                    occurences = int(temp[1])
                    valeur = int(temp[2])
                    joker = temp[3]
                    self.lettres_def[lettre] = valeur
                    for _ in range(occurences):
                        self.jetons_libres.append(Jeton(lettre, valeur, joker))

        with open('dic/{}.txt'.format(self.langue), 'r') as dic:
            self.dictionnaire = set([x[:-1].upper() for x in dic.readlines() if len(x[:-1]) > 1])

    def jouer(self, cases=None):
        """
        La fonction démarre une partie de scrabble.
        Pour une nouvelle partie de scrabble,
        - un nouvel objet Plateau est créé;
        - un nouvel objet Jeu est créé
        - on part les horloges
        :param cases: Liste des cases, None par défaut, passé en argument quand on charge une partie.
        """
        # Active les options "nouvelle partie" et "sauvegarder partie du menu"
        self.fichier.entryconfig(0, state="normal")
        self.fichier.entryconfig(1, state="normal")
        self.fichier.entryconfig(2, state="normal")

        self.presentation.entryconfig(0, state="normal")
        self.presentation.entryconfig(1, state="normal")

        self.jeu = Jeu(self.content, self)

        # Horloges
        self.set_clock()
        self.clock()
        if self.difficulte == 'difficile':
            self.jeu.timer.lift()
            self.set_timer()
            self.tick()

        # Set le plateau
        self.plateau = Plateau(self, self.content, self.PIXELS_PAR_CASE, cases)
        self.plateau.grid(row=1, column=0, rowspan=5, sticky=NSEW)

    def determiner_case(self, event):
        """
        Permet de déterminer la case clickée par un event de souris
        :param event: l'event de souris
        :return: (tuple) tuple à 3 éléments: ligne du plateau, colonne du plateau, case
        """
        ligne = event.y // self.plateau.pixels_par_case
        col = event.x // self.plateau.pixels_par_case

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

            self.plateau.dessiner()

            self.joueur_actif.jeton_actif = None

            unbind_redeposer(self)
            unbind_poser(self)
            self.after(500, lambda : bind_reprendre(self))

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

                unbind_redeposer(self)
                unbind_poser(self)
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
            pos = event.x // self.PIXELS_PAR_CASE
            try:
                self.joueur_actif.jeton_actif = self.joueur_actif.retirer_jeton(pos)

                assert isinstance(self.joueur_actif.jeton_actif, Jeton)
                assert self.joueur_actif.chevalet[pos] is None

                self.chevalet_actif.delete('chevalet{}'.format(pos))

                self.after(500, lambda : bind_redeposer(self))
                bind_poser(self)
            except (PositionChevaletException, AssertionError) as e:
                print(e)

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
            try:
                jeton = case.retirer_jeton()

                self.plateau.jetons_places.remove(jeton)
                self.joueur_actif.jeton_actif = jeton
                self.plateau.positions.remove((ligne, col))

                self.plateau.dessiner()

                bind_redeposer(self)
                bind_poser(self)
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
        # Vérifie si le joueur a placé des jetons
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
                    lettre = askstring('Joker', "Entrez la lettre que vous souhaitez attribuer au joker.\n"
                                                "Si vous avez mis plusieurs jokers, "
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
            mots_non_permis = [mot for mot in mots if not mot_permis(mot, self.dictionnaire)]

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

        mots_str = mots[0]
        mots.remove(mots[0])
        if len(mots) > 1:
            for mot in mots:
                mots_str += ", {}".format(mot)

        log = "Tour {}: {} a obtenu {} points.\n  Mots placés: {}.\n  Le tour a pris {} sec.\n".format(self.tour, self.joueur_actif.nom, score, mots_str, self.temps)
        self.ecrire_log(log)

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
        bind_prendre(self)

    def verifier_jetons_sur_le_plateau(self):
        """
        Vérifie si le joueur a placé des jetons dans le tour courant.
        :return: bool, True si des jetons ont été placés sur le plateau dans le tour courant, false sinon
        """
        return len(self.plateau.positions) != 0 or len(self.plateau.jetons_places) != 0

    def passer_un_tour(self):
        """
        Permet à un joueur de passer son tour.
        - vérifier que le joueur n'a pas placé de jetons sur le plateau
        - changer de joueur
        :return: aucun retour
        """
        if self.verifier_jetons_sur_le_plateau():
            rep = askyesno(message="Vous avez placé des jetons sur le plateau. Êtes-vous certain de vouloir passer votre tour?\n"
                                   "Les jetons placés seront retournés dans votre jeu.")
            if rep:
                self.reprendre_tous_les_jetons()
            else:
                return

        log = "Tour {}: {} a passé son tour.\n  Le tour a pris {} sec.\n".format(self.tour, self.joueur_actif.nom, self.temps)
        self.ecrire_log(log)

        self.changer_joueur()

    def abandonner(self):
        """
        Retire un joueur de la liste des joueurs
        :return: Aucun return
        """
        rep = askyesno(message="Êtes-vous certain de vouloir abandonner la partie?")
        if rep:
            if self.verifier_jetons_sur_le_plateau():
                self.reprendre_tous_les_jetons()

            log = "Tour {}: {} a abandonné la partie.\n  Le tour a pris {} sec.\n".format(self.tour, self.joueur_actif.nom, self.temps)
            self.ecrire_log(log)

            abandonner = self.joueur_actif
            self.changer_joueur()
            self.joueurs.remove(abandonner)
        else:
            return

        # Vérifie si la partie est terminée
        if self.partie_terminee():
            return

    def demander_jetons_a_changer(self):
        """
        Interface graphique pour changer les jetons
        - unbinder la fonction prendre
        - afficher le sac a jeton et les boutons
        - binder la fonction jeter
        :return: Aucun return
        """
        if self.verifier_jetons_sur_le_plateau():
            rep = askyesno(
                message="Vous avez placé des jetons sur le plateau. "
                        "Êtes-vous certain de vouloir échanger des jetons et passer votre tour?\n"
                        "Les jetons placés seront retournés dans votre jeu.")
            if rep:
                self.reprendre_tous_les_jetons()
            else:
                return

        # Bindings
        unbind_prendre(self)
        bind_jeter(self)

        # Affichage de l'interface
        self.jeter.lift()

        # Désactive les boutons d'actions
        self.desactiver_btn_actions()

    def jeter_jeton(self, event):
        """
        Permet de retirer un jeton du chevalet du joueur et le placer dans le chevalet des jetons à jeter.
        Utilisé dans l'interface pour changer les jetons.
        :param event: Le clic de souris ayant déclenché l'évènement
        :return: aucun
        :exception: On arrête l'exécution si la position sur le chevalet est incorrecte ou qu'il ne reste plus de jetons disponibles.
        """
        pos = event.x // self.PIXELS_PAR_CASE

        # Théoriquement les bindings font en sorte qu'il est impossible de déclencher l'événement avec une mauvaise position, mais juste au cas.
        if 0 > pos > self.chevalet_actif.TAILLE_CHEVALET:
            raise PositionChevaletException

        if len(self.joueur_actif.jetons_jetes) >= len(self.jetons_libres):
            showwarning(message="Il n'y a plus de jetons disponibles dans le sac à jetons.")
            return

        jeton_retire = self.joueur_actif.retirer_jeton(pos)

        self.joueur_actif.jetons_jetes.append(jeton_retire)

        x1, y1, x2, y2, delta = coord_pos(pos, self.PIXELS_PAR_CASE)
        dessiner_jeton(self.sac_a_jetons, x1, y1, x2, y2, delta, jeton_retire, 'chevalet{}'.format(pos))
        self.chevalet_actif.delete('chevalet{}'.format(pos))

    def changer_jetons(self):
        """
        Change les jetons sélectionnés par le joueur dans l'interface pour changer les jetons.
        - On tire de nouveaux jetons dans le sac à jetons
        - On ajoute les jetons tirés au chevalet du joueur
        - On retourne les jetons jetés par le joueur dans le sac à jetons
        - unbind jeter_jeton et rebind prendre jeton
        - cacher le frame pour changer les jetons
        - On passe au joueur suivant
        :return: Aucun return
        """
        unbind_jeter(self)

        # Piger de nouveaux jetons et retourner les jetons jetés au sac à jetons
        jetons_a_ajouter = self.tirer_jetons(self.joueur_actif.nb_a_tirer)
        for jeton in jetons_a_ajouter:
            self.joueur_actif.ajouter_jeton(jeton)
        self.jetons_libres = self.jetons_libres + self.joueur_actif.jetons_jetes

        # Cacher l'interface pour changer les jetons
        bind_prendre(self)
        self.jeter.lower()

        # Réactive les boutons d'actions
        self.activer_btn_actions()

        # Set log
        log = "Tour {}: {} a changé {} jetons.\n  Le tour a pris {} sec.\n".format(self.tour, self.joueur_actif.nom, len(self.joueur_actif.jetons_jetes), self.temps)
        self.ecrire_log(log)

        # Passer un tour
        self.joueur_actif.jetons_jetes = []
        self.changer_joueur()

    def annuler_changer_jetons(self):
        """
        Fonction qui est déclenchée lorsque le joueur appuie sur le bouton annuler dans l'interface pour changer les jetons.
        La fonction doit:
        - Remettre les jetons dans le chevalet du joueur.
        - unbind jeter_jeton et rebind prendre_jeton
        - cacher le frame pour changer les jetons
        """
        # Remettre les jetons jetés dans le chevalet du joueur
        for jeton in self.joueur_actif.jetons_jetes:
            self.joueur_actif.ajouter_jeton(jeton)

        self.chevalet_actif.dessiner(self.joueur_actif)
        self.joueur_actif.jetons_jetes = []

        # Cacher l'interface pour changer les jetons et ajuster les bindings
        unbind_jeter(self)
        bind_prendre(self)
        self.jeter.lower()

        # Réactive les boutons d'actions
        self.activer_btn_actions()

    def desactiver_btn_actions(self):
        """
        Fonction utilitaire pour désactiver les boutons d'action de l'interface du joueur lorsqu'il est en mode "changer les jetons".
        Permet d'éviter les erreurs si le joueur oublie qu'il est en mode changer les jetons.
        """
        self.btn_jouer.config(state="disabled")
        self.btn_annuler.config(state="disabled")
        self.btn_passer.config(state="disabled")
        self.btn_changer.config(state="disabled")
        self.btn_abandonner.config(state="disabled")

    def activer_btn_actions(self):
        """
        Fonction utilitaire pour réactiver les boutons d'action du joueur lorsqu'il quitte le mode "changer les jetons".
        """
        self.btn_jouer.config(state="normal")
        self.btn_annuler.config(state="normal")
        self.btn_passer.config(state="normal")
        self.btn_changer.config(state="normal")
        self.btn_abandonner.config(state="normal")

    def changer_joueur(self, charger=False, tour=0):
        """
        Change le joueur. C'est l'action de passer le tour au prochain joueur. La méthode change le joueur actif et affiche dans l'interface les infos du nouveau joueur.
        La méthode vérifie aussi si la partie est terminée.
        :param charger: Bool, False par défaut, True quand une partie est chargée
        :param tour ; int, 0 par défaut, si on charge une partie le tour sera affecté
        :return: Aucun return
        """
        if self.partie_terminee():
            return

        # update des points du joueur actif
        if self.tour == 0:
            pass
        else:
            i = self.joueurs.index(self.joueur_actif)
            self.labels_points[i].config(text="{}".format(self.joueur_actif.points))

        # On passe au joueur suivant et on incrémente le tour de la partie, si on ne charge pas une partie
        if charger is False:
            self.joueur_suivant()
            self.tour += 1
        else:
            self.tour = tour

        # On détermine le message à afficher
        if self.tour == 1:
            msg = "Tour {}\nLa partie va commencer avec le {}".format(self.tour, self.joueur_actif.nom)
        else:
            msg = "Tour {}\nC'est le tour de {}".format(self.tour, self.joueur_actif.nom)

        # On pige les jetons

        try:
            for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
                self.joueur_actif.ajouter_jeton(jeton)
        except SacVideException as e:
            showwarning(message=e)

        # On update l'affichage
        self.message.set(msg)
        self.nom_joueur.set(self.joueur_actif.nom)
        self.chevalet_actif.dessiner(self.joueur_actif)
        if self.affichage_suggestions:
            self.afficher_suggestions()
        self.sac_a_jetons_label.config(text="Il reste {} jetons dans le sac.".format(len(self.jetons_libres)))

        # Horloges
        self.set_clock()
        if self.difficulte == "difficile":
            self.set_timer()

        # Bindings
        bind_prendre(self)

        # Autosave
        self.sauvegarder_partie(autosave=True)

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
        if len(self.jetons_libres) < 1 or len(self.joueurs) < 2:
            self.desactiver_btn_actions()
            unbind_prendre(self)
            log = "Partie terminée, {} est le gagant!".format(self.determiner_gagnant().nom)
            self.ecrire_log(log)
            self.message.set(log)
            showinfo(message=log)

            # Cancel les horloges
            self.temps_label.after_cancel(self.jobs['clock'])
            if self.jobs['timer'] is not None:
                self.timer_label.after_cancel(self.jobs['timer'])

            # Désactive la sauvegarde
            self.fichier.entryconfig(1, state="disabled")
            self.fichier.entryconfig(2, state="disabled")

            return True
        else:
            return False

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
        :exception: Levez une exception avec assert si n ne respecte pas la condition n>=0. Si le nombre à tirer excède le nombre de jetons libres dans le sac
        à jetons, on ajuste n au nombre de jetons restants. S'il ne reste plus de jetons, on lève une exception de type SacVideException.
        """
        assert n >= 0, "n doit être supérieur à 0"

        if len(self.jetons_libres) == 0:
            raise SacVideException("Il n'y a plus de jetons libres dans le sac à jetons.")

        if n > len(self.jetons_libres):
            n = len(self.jetons_libres)

        # On mélange les jetons dans le sac
        shuffle(self.jetons_libres)

        # On prend n jetons et on les enlève du sac
        jetons_tires = self.jetons_libres[:n]
        self.jetons_libres = self.jetons_libres[n:]

        # Écriture du log
        log = "{} pige {} jetons.\n".format(self.joueur_actif.nom, len(jetons_tires))
        self.ecrire_log(log)

        return jetons_tires

    def set_clock(self):
        """
        Remet l'horloge à 0 et update l'affichage du temps dans l'interface.
        :return:
        """
        self.temps = 0
        self.temps_label['text'] = self.temps

    def clock(self):
        """
        Fonction qui sert d'horloge pour garder le compte du temps utilisé pour chaque tour.
        :return:
        """
        self.temps += 1
        self.temps_label['text'] = self.temps
        self.jobs['clock'] = self.temps_label.after(1000, self.clock)

    def set_timer(self):
        """
        Fonction utilitaire simple qui reset le timer au temps permis (difficulté 'difficile' utilisant les règles officielles)
        """
        self.timer = 120
        self.timer_label['text'] = self.timer

    def tick(self):
        """
        Fonction responsable de faire fonctionner le timer pour limiter le temps alloué par tour dans la difficulté 'difficile' officielle.
        Est aussi responsable de l'affichage du timer dans l'interface
        """
        self.timer -= 1
        if self.timer == 0:
            self.temps_ecoule()
        self.timer_label['text'] = self.timer
        self.jobs['timer'] = self.timer_label.after(1000, self.tick)

    def temps_ecoule(self):
        """
        Fonction appelée lorsque le temps par tour alloué est écoulé dans la version 'difficile' utilisant les règles officielles.
        Reprend tous les jetons placés et les retourne dans le chevalet du joueur avant de changer de joueur.
        """
        showwarning('Temps écoulé', 'Vous avez épuisé tout le temps permis! Vous passez votre tour.')
        self.reprendre_tous_les_jetons()
        self.annuler_changer_jetons()
        self.changer_joueur()

    def sauvegarder_partie(self, nouvelle_sauvegarde=True, autosave=False):
        """
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :param: nouvelle_sauvegarde: bool, True si on souhaite faire une nouvelle sauvegarde (Enregistrer sous).
        False, si on souhaite enregistrer sous le même nom que la précédante sauvegarde. Ce paramètre permet de sauvegarder plusieurs
        fois une partie sans avoir à écrire le nom du fichier à chaque fois.
        :param: autosave: bool, True si c'est une sauvegarde automatique, False autrement.
        :return: Aucun
        """
        if self.verifier_jetons_sur_le_plateau():
            rep = askyesno(message="Vous avez placé des jetons sur le plateau. Êtes-vous certain de vouloir sauvegarder?\n"
                                   "Les jetons placés seront retournés dans votre chevalet avant la sauvegarde.")
            if rep:
                self.reprendre_tous_les_jetons()
            else:
                return

        if autosave:
            nom_fichier = "{}/saves/autosave.pkl".format(self.path)
        elif self.save is None or nouvelle_sauvegarde:
            nom_fichier = asksaveasfilename(title="Sauvegarder une partie", filetypes=[('pkl', '*.pkl'), ('txt', '*.txt')], initialdir="{}/saves".format(self.path))
            # Version alternative si filedialog est buggy
            # nom_fichier = askstring("Sauvegarder une partie", "Entrez le nom de la sauvegarde avec l'extension .pkl")
        else:
            nom_fichier = self.save

        if nom_fichier is not None and nom_fichier != '':
            try:
                with open(nom_fichier, "wb") as f:
                    pickle.dump(self.langue, f)
                    pickle.dump(self.joueurs, f)
                    position_joueur_actif = self.joueurs.index(self.joueur_actif)
                    pickle.dump(position_joueur_actif, f)
                    pickle.dump(self.jetons_libres, f)
                    pickle.dump(self.plateau.cases, f)
                    pickle.dump(self.tour, f)
                    pickle.dump(self.difficulte, f)
                    pickle.dump(self.log.get(1.0, "end-1c"), f)

            except Exception as e:
                showwarning("Échec", "Échec de la sauvegarde")
                print(e)
                return
            else:
                if not autosave:
                    self.save = nom_fichier

    def charger_partie(self):
        """
        Méthode permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment.
        :return:
        """
        self.verifier_avant_de_quitter()

        nom_fichier = askopenfilename(title="Charger une partie sauvegardée", filetypes=[('pkl', '*.pkl'), ('txt', '*.txt')], initialdir="{}/saves".format(self.path))

        # Version alternative si filedialog est buggy
        # nom_fichier = askstring("Charger une partie", "Entrez le chemin d'accès de la sauvegarde avec l'extension .pkl")

        if nom_fichier is not None and nom_fichier != '':
            try:
                with open(nom_fichier, "rb") as f:
                    langue = pickle.load(f)
                    joueurs = pickle.load(f)
                    position_joueur_actif = pickle.load(f)
                    jetons_libres = pickle.load(f)
                    cases = pickle.load(f)
                    tour = pickle.load(f)
                    difficulte = pickle.load(f)
                    log = pickle.load(f)

                    # Vérification de l'intégrité des données chargées.
                    if langue not in Scrabble.LANGUES_DISPONIBLES:
                        raise FichierCorrompu
                    if not isinstance(joueurs, list):
                        raise FichierCorrompu
                    if not all([isinstance(joueur, Joueur) for joueur in joueurs]):
                        raise FichierCorrompu
                    if not isinstance(position_joueur_actif, int):
                        raise FichierCorrompu
                    if not position_joueur_actif in range(len(joueurs)):
                        raise FichierCorrompu
                    if not isinstance(jetons_libres, list):
                        raise FichierCorrompu
                    if not all(isinstance(jeton, Jeton) for jeton in jetons_libres):
                        raise FichierCorrompu
                    if not isinstance(cases, list):
                        raise FichierCorrompu
                    if not all([isinstance(case, Case) for ligne in cases for case in ligne]):
                        raise FichierCorrompu
                    if not isinstance(tour, int):
                        raise FichierCorrompu
                    if tour < 1:
                        raise FichierCorrompu
                    if not isinstance(difficulte, str):
                        raise FichierCorrompu
                    if difficulte not in Scrabble.DIFFICULTES_DISPONIBLES:
                        raise FichierCorrompu
                    if not isinstance(log, str):
                        raise FichierCorrompu

            except (pickle.UnpicklingError, FichierCorrompu):
                showwarning(message="Le fichier que vous tentez de charger semble corrompu.")
                return

            except FileNotFoundError:
                showwarning(message="Le fichier spécifié est introuvable.")
                return

            # on détruit la fenêtre principale et on la recrée pour être sûr qu'elle est "propre"
            self.content.destroy()
            self.config_content()
            self.reset_partie()

            # On initialise la partie
            self.initialiser_partie(len(joueurs), langue, difficulte, joueurs=joueurs)

            #set param
            self.joueur_actif = self.joueurs[position_joueur_actif]
            self.jetons_libres = list(jetons_libres)

            # On lance la partie
            self.jouer(cases)
            self.changer_joueur(charger=True, tour=tour)

            # On écrit le log
            self.log.delete(1.0, END)
            self.ecrire_log(log)

    def assistance(self):
        """
        fonction qui propose des mots au joueur actif selon les jetons dans son chevalet.
        :return: str: suggestion des mots prêt à afficher
        """
        lettres_chevalet = [jeton.lettre for jeton in self.joueur_actif.chevalet if jeton is not None]
        suggestions = set()

        if self.plateau.est_vide():
            suggestions.update(self.chercher_dico(lettres_chevalet, suggestions))

        else:
            lettres_plateau = []
            for ligne in range(len(self.plateau.cases)):
                for colonne in range(len(self.plateau.cases[ligne])):
                    if self.plateau.cases[ligne][colonne].jeton_occupant is not None:
                        if self.plateau.cases[ligne][colonne].jeton_occupant.lettre not in lettres_plateau:
                            lettres_plateau.append(self.plateau.cases[ligne][colonne].jeton_occupant.lettre)

            for lettre in lettres_plateau:
                lettres_chevalet.append(lettre)
                suggestions.update(self.chercher_dico(lettres_chevalet, suggestions))
                del lettres_chevalet[-1]

        suggestions_tries = []
        for mot in suggestions:
            suggestions_tries.append(self.calculer_points(mot))
        suggestions_tries.sort(key=lambda tup: tup[1], reverse=True)
        return suggestions_tries

    def chercher_dico(self, lettres, suggestions):
        """
        Fonction qui cherche dans le dictionnaire des suggestions de mots selon une liste de lettres
        :param: lettres: list, liste de lettres provenant du chevalet et du plateau
        :param: suggestions: list, liste des mots suggérés à date.
        :return: list: suggestions est la liste de mots suggérés.
        """
        for mot in self.dictionnaire:
            lettres_a_verifier = lettres[:]
            pas_trouve = False
            if mot == '':
                break
            for lettre in mot:
                if lettre not in lettres_a_verifier:
                    pas_trouve = True
                    break
                else:
                    lettres_a_verifier.remove(lettre)

            if not pas_trouve:
                suggestions.add(mot)

        return suggestions

    def calculer_points(self, mot):
        """
        Permet de calculer les points d'un mot selon les valeurs des lettres du mot.
        Ne tiens pas compte du placement sur le plateau.
        :param mot: str, mot dont il faut calculer les points.
        :return: tuple, constitué du mot et des points
        """
        points = 0

        for lettre in mot:
            points += self.lettres_def[lettre]

        return mot, points

    def afficher_suggestions(self):
        """
        Update l'affichage des suggestions dans l'espace réservé à cette fin dans l'interface.
        :return: aucun
        """
        self.suggestions.config(state="normal")
        self.suggestions.delete(1.0, END)
        for mot in self.assistance():
            mot_str = "{}, {} points\n".format(mot[0], mot[1]).capitalize()
            self.suggestions.insert(END, mot_str)

        self.suggestions.config(state="disabled")

    def ecrire_log(self, log):
        """
        Permet d'écrire un message dans l'historique de la partie dans l'interface.
        :param log: Str, Message à ajouter au log.
        :return: aucun
        """
        self.log.config(state="normal")
        self.log.insert(1.0, log)
        self.log.config(state="disabled")

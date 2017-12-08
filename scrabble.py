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
from tkinter import Toplevel
from tkinter import filedialog

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

        # Declare parameters
        self.liste_langue = ['fr', 'en']
        self.langue='fr'    # La langue par défaut est le français.
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
        self.content.grid_rowconfigure(2, weight=1)

        # Création du menu
        barre_menu = Menu(self)
        fichier = Menu(barre_menu, tearoff=0)
        fichier.add_command(label="Nouvelle partie", command=Scrabble)
        fichier.add_command(label="Sauvegarder la partie", command=self.demande_sauvegarder_partie)  # TODO: state active quand une partie est en cours
        fichier.add_command(label="Charger une partie", command=self.demander_charger_partie)  # TODO: commande qui ouvre une fenetre avec un text pour charger la partie
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
        Label(accueil, text="Choisissez la langue du jeu:", font=("Times", 16)).grid(row=1, columnspan=4, pady=self.PADY)

        # Choix des langues
        langue = StringVar()
        langue.set('fr')
        Radiobutton(accueil, text='Français', variable=langue, value='fr').grid(column=0, row=2, columnspan=2, sticky=E)
        Radiobutton(accueil, text='English', variable=langue, value='en').grid(column=2, row=2, columnspan=2, sticky=W)

        # Nombre des joueurs
        Label(accueil, text="Choisissez le nombre de joueurs:", font=("Times", 16)).grid(row=3, column=0, columnspan=4, pady=self.PADY)
        nb_joueurs = IntVar()
        nb_joueurs.set(2)
        Radiobutton(accueil, text='2 joueurs', variable=nb_joueurs, value=2).grid(column=0, row=4)
        Radiobutton(accueil, text='3 joueurs', variable=nb_joueurs, value=3).grid(column=1, row=4)
        Radiobutton(accueil, text='4 joueurs', variable=nb_joueurs, value=4).grid(column=2, row=4)
        Radiobutton(accueil, text='Jouer contre l\'ordinateur', variable=nb_joueurs, value=1, state=DISABLED).grid(column=3, row=4)

        # Débuter la partie
        Button(accueil, text="Commencer une nouvelle partie", command=lambda: self.demarrer_partie(accueil, nb_joueurs.get(), langue.get())).grid(row=5, column=0, columnspan=2, pady=self.PADY)
        Button(accueil, text="Charger une partie existante", command=self.demander_charger_partie, state=DISABLED).grid(row=5, column=2, columnspan=2, pady=self.PADY)


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
        :param langue: str, abbréviation à 2 lettres de la langue
        Dépendamment de la langue, on doit ouvrir, lire, charger en mémoire le bon dictionnaire.
        Les dictionnaires sont dans le dossier dic et sont nommés par l'abbéviation à deux lettres de la langue du dictionnaire.
        Exemple: le chemin d'accès du dictionnaire français est 'dic/fr.txt' et celui du dictionnaire anglais est 'dic/en.txt'
        Ensuite il suffit d'extraire les mots contenus pour construire un set avec le mot clé set.
        Aussi, grâce à la langue vous devez être capable de créer tous les data de départ et les mettre dans jetons_libres.

        Pour savoir combien de data créés pour chaque langue vous pouvez regarder à l'adresse:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble

        :exception: Levez une exception avec assert si la langue n'est ni fr ou en ou si nb_joueur < 2 ou > 4.
        """
        assert 2 <= nb_joueurs <= 4
        assert langue.lower() in self.liste_langue
        self.langue = langue.lower()
        self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]

        with open('data/{}.txt'.format(self.langue), 'r') as data:
            self.jetons_libres = []
            for line in data.readlines():
                temp = line.split(',')
                lettre = str(temp[0])
                occurences = int(temp[1])
                valeur = int(temp[2])
                for _ in range(occurences):
                    self.jetons_libres.append(Jeton(lettre, valeur))

        with open('dic/{}.txt'.format(self.langue), 'r') as dic:
            self.dictionnaire = set([x[:-1].upper() for x in dic.readlines() if len(x[:-1]) > 1])


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
        self.plateau.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=NSEW)

        # Set le tableau d'affichange
        tableau = Frame(self.content)
        tableau.grid(row=0, column=1, columnspan=3, sticky=NSEW)
        Label(tableau, textvariable=self.message).grid(row=0)
        Label(tableau, textvariable=self.pointage).grid(row=1)

        # Set les joueurs
        self.affichage_joueur = Frame(self.content)
        self.affichage_joueur.grid(row=1, column=1, rowspan=1, columnspan=3, sticky=NSEW)
        Label(self.affichage_joueur, textvariable=self.nom_joueur).grid(row=0, column=0, columnspan=3)
        self.chevalet_actif = Canvas(self.affichage_joueur, height=self.PIXELS_PAR_CASE, width=self.PIXELS_PAR_CASE*Joueur.TAILLE_CHEVALET, bg='#f5ebdc')
        self.chevalet_actif.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Set les boutons d'actions
        btn_jouer = Button(self.affichage_joueur, text="Joueur le tour", command=self.jouer_un_tour)
        btn_passer = Button(self.affichage_joueur, text="Passer le tour", command=self.passer_un_tour)
        btn_changer = Button(self.affichage_joueur, text="Changer les jetons", command=self.demander_jetons_a_changer)
        btn_quitter = Button(self.affichage_joueur, text="Quitter la partie", command=self.quitter)

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
            dessiner_jeton(self.plateau, x1, y1, x2, y2, delta, self.joueur_actif.jeton_actif, ('jeton','jeton_place', "jeton_{}_{}".format(ligne, col)))

            self.joueur_actif.jeton_actif = None

            self.unbind_redeposer()
            self.unbind_poser()
            self.after(500, self.bind_reprendre)
        except (CaseOccupeeException, AssertionError) as e:
            messagebox.showwarning(message=e)
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
        pos = floor(event.x / self.PIXELS_PAR_CASE)
        jeton_retire = self.joueur_actif.retirer_jeton(pos)
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
            messagebox.showinfo(message="Vous n'avez pas placé de jetons!\nSi vous ne désirez pas jouer ce tour-ci, "
                                           "veuillez sélectionner le bouton 'Passer le tour'")
            return

        # Vérifie la validité des positions des jetons placés
        try:
            self.plateau.valider_positions(self.plateau.positions)
        except (CasesNonEnLigneException, PasDeCasesAdjacentes, CaseVideDansMot, CentreNonUtilise) as e:
            messagebox.showwarning(message=e)
            return

        # Vérifie si les mots sont permis
        try:
            mots, score = self.plateau.mots_score_obtenus(self.plateau.positions)
            mots_non_permis = [mot for mot in mots if not self.mot_permis(mot)]
            if len(mots_non_permis) != 0:
                msg = "Un ou plusieurs mots ne sont pas permis:\n"
                for mot in mots_non_permis:
                    msg = msg + "- " + mot + "\n"
                raise MotNonPermisException(msg)
            # Si toutes les lettres sont placés, on ajoute 50 points, car c'est un Scrabble!
            if len(self.plateau.jetons_places) == Joueur.TAILLE_CHEVALET:
                messagebox.showinfo('Scrabble!', 'Félicitations! Vous avez placé tous vos data!\nVous obtenez 50 points boni!')
                score += 50
        except MotNonPermisException as e:
            messagebox.showwarning(message=e)
            return

        self.joueur_actif.ajouter_points(score)
        self.plateau.positions = []
        self.plateau.jetons_places = []
        self.changer_joueur()

    def passer_un_tour(self):
        """
        Permet à un joueur de passer son tour.
        - vérifier que le joueur n'a pas placé de jetons sur le plateau
        - changer de joueur
        :return: aucun retour
        """
        # Vérifie si le joueur a placé des jetons
        if len(self.plateau.positions) != 0 or len(self.plateau.jetons_places) != 0:
            messagebox.showinfo(message="Vous avez placé de jetons!\nSi vous désirez passer votre tour, "
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
            messagebox.showinfo(message="Vous avez placé de jetons!\nSi vous désirez abandonner, "
                                        "retirez vos jetons du plateau.\n"
                                        "Sinon, sélectionnez 'Jouer un tour'")
            return

        quitter = self.joueur_actif
        self.changer_joueur()
        self.joueurs.remove(quitter)

        # Vérifie si la partie est terminée
        if self.partie_terminee():
            messagebox.showinfo('Partie terminée', '{} est le gagnant! Félicitations!'.format(self.determiner_gagnant().nom))
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
            messagebox.showinfo(message="Vous avez placé de jetons!\nSi vous désirez changer des jetons, "
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

    def changer_joueur(self):
        """
        Change le joueur. C'est l'action de passer le tour au prochain joueur. La méthode change le joueur actif et affiche dans l'interface les infos du nouveau joueur.
        La méthode vérifie aussi si la partie est terminée.
        -
        :return: Aucun return
        """
        # Vérification si la partie est terminée
        if self.partie_terminee():
            messagebox.showinfo('Partie terminée', '{} est le gagnant! Félicitations!'.format(self.determiner_gagnant().nom))
            return
            # TODO: vérifier pour cette condition si l'exécution se fait bien et potentiellement améliorer l'action

        # On passe au joueur suivant et on incrémente le tour de la partie
        self.joueur_suivant()
        self.plateau.tour += 1

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

    def sauvegarder_partie(self, nom_fichier):
        """
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: True si la sauvegarde s'est bien passé, False si une erreur s'est passé durant la sauvegarde.
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

        try:
            with open(nom_fichier, "wb") as f:
                pickle.dump(self.langue, f)
                pickle.dump(self.joueurs, f)
                pickle.dump(self.plateau.cases, f)
            self.fenetre_sauv.destroy()

        except:
            print("echec")  # et ici...
            return False

        # ici éventuellement c'est à bouger dans charger évidemment -> je l'ai mis la pour accélerer les tests au début.
        with open(nom_fichier, "rb") as f:
            langue = pickle.load(f)
            joueurs = pickle.load(f)
            print(langue, joueurs)
            print(joueurs[0].points)

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
            print(objet)
        return objet

    def demande_sauvegarder_partie(self):

        # Commentaire: pourquoi tu n'utilises pas le module tkFileDialog??
        # Ça va vrmt te simplifier la vie. cherches ça sur google et tu vas trouver. je t'ai envoyé un lien dans skype aussi!
        # self.nom_fichier = filedialog.asksaveasfilename(initialdir="/", title="Sélectionnez un fichier", filetypes=(("all files", "*.*"),))
        # print(self.nom_fichier)
        #
        # self.sauvegarder_partie(self.nom_fichier)

       self.fenetre_sauv = Toplevel(self)
       self.fenetre_sauv.title("Sauvegarder")
       cadre_label_entry = Frame(self.fenetre_sauv, padx=10, pady=10)
       cadre_label_entry.grid(row=0)

       label_sauvegarde = Label(cadre_label_entry, text="Entrez le nom de la sauvegarde:", padx=10, pady=10)
       label_sauvegarde.grid(row=0)

       nom_fichier =StringVar()

       entry_sauvegarde = Entry(cadre_label_entry, textvariable=nom_fichier)
       entry_sauvegarde.grid(row=1)

       cadre_btn = Frame(self.fenetre_sauv, padx=10, pady=10)
       cadre_btn.grid(row=1)
       btn_ok = Button(cadre_btn, text="Sauvegarder", padx=10, pady=10,
                       command=lambda: self.sauvegarder_partie(nom_fichier.get()))
       btn_ok.grid(row=0, column=0)
       btn_cancel = Button(cadre_btn, text="Annuler",  padx=10, pady=10, command=self.fenetre_sauv.destroy)
       btn_cancel.grid(row=0, column=2)

    def demander_charger_partie(self):

        self.nom_fichier = filedialog.askopenfilename(initialdir="/", title="Sélectionnez un fichier",
                                                      filetypes=(("all files", "*.*"),))
        print(self.nom_fichier)
        self.charger_partie(self.nom_fichier)


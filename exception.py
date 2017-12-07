"""
Fichier python contenant les classes d'exeption. J'ai pensé à les mettres dans un fichier à part.

"""


class PositionInvalideException(Exception):
    pass


class MotNonPermisException(Exception):
    pass


class CaseOccupeeException(Exception):
    pass


class CaseVideException(Exception):
    pass

class CasesNonEnLigneException(Exception):
    pass

class CentreNonUtilise(Exception):
    pass

class PasDeCasesAdjacentes(Exception):
    pass

class CaseVideDansMot(Exception):
    pass

class CaseMultiException(Exception):
    pass


class CaseTypeException(Exception):
    pass


class NomInvalideException(Exception):
    pass


class PositionChevaletException(Exception):
    pass


class JetonLettreException(Exception):
    pass


class JetonValeurException(Exception):
    pass


class AutreExeption(Exception):
    pass


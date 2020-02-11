# coding: utf-8

"""
    Module qui contient des données que l'on pourra afficher dans tous les templates
"""

# =================================================================================================
# PARAMETRES GLOBAUX
# =================================================================================================

__author__ = 'Julien LEPAIN'
__version__ = '1.0'
__maintainer__ = 'Julien LEPAIN'
__date__ = '01/2020'
__status__ = 'dev'


# ==================================================================================================
# IMPORTS
# ==================================================================================================

from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import constant_time_compare, salted_hmac
from django.conf import settings

from lyre_d_alliez.secret_data import SECRET_KEY

from .models import Jeton

from datetime import datetime


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ==========================================
class AccountCreationTokenGenerator(object):
    """
        Objet utilisé afin de générer and vérifier des jetons dans la cadre d'une création de profil membre

        Librement inspiré de la classe "PasswordResetTokenGenerator" de la librairie django.contrib.auth.tokens
    """

    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    secret = SECRET_KEY

    # =============================================
    def make_token(self, random_id_1, random_id_2):
        """
            Retourne un jeton qui peut être utilisé une seule fois pour remplir
            le formulaire de création d'un compte membre pour une adresse email donnée.

            Le jeton est créé à partir de deux identifiants générés aléatoirements.

            :param random_id_1: premier identifiant généré alétoirement
            :type random_id_1: str

            :param random_id_2: second identifiant généré alétoirement
            :type random_id_2: str

            :return: le jeton
            :rtype: str
        """

        return self._make_token_with_timestamp(random_id_1, random_id_2, self._num_days(self._today()))

    # =====================================================
    def check_token(self, random_id_1, random_id_2, jeton):
        """
            Vérifie que le jeton est correct les deux identifiants générés aléatoirements.

            :param random_id_1: premier identifiant généré alétoirement
            :type random_id_1: str

            :param random_id_2: second identifiant généré alétoirement
            :type random_id_2: str

            :param jeton: adresse email donnée
            :type jeton: str

            :return: le statut de la vérification
            :rtype: bool
        """

        if not (random_id_1 and random_id_2 and jeton):

            return False

        # Récupération du jeton
        try:

            nombre_de_jours_b36, hash = jeton.split("-")

        except ValueError:

            return False

        try:

            nombre_de_jours = base36_to_int(nombre_de_jours_b36)

        except ValueError:

            return False

        # Vérification que le jeton actuel n'a pas déjà été utilisé
        objet_jeton_courant = Jeton.objects.filter(valeur__iexact=jeton)

        if objet_jeton_courant.exists():

            jeton_courant = objet_jeton_courant.first()

            if jeton_courant.deja_utilise:

                return False

            else:

                # Vérification que le nombre de jours n'a pas été falsifié
                if not constant_time_compare(self._make_token_with_timestamp(random_id_1, random_id_2, nombre_de_jours), jeton):

                    return False

                # Vérification que le nombre de jours est bien dans les limites.
                if (self._num_days(self._today()) - nombre_de_jours) > settings.PASSWORD_RESET_TIMEOUT_DAYS:

                    return False

                jeton_courant.deja_utilise = True
                jeton_courant.save()

                return True

        else:

            return False

    # ==============================================================================
    def _make_token_with_timestamp(self, random_id_1, random_id_2, nombre_de_jours):
        """
            Méthode (privée) qui permet de créer un jeton à partir de :

            - deux identifiants générés aléatoirements ;
            - du nombre de jours entre la date du jour et le 1er janvier 2001.

            :param random_id_1: premier identifiant généré alétoirement
            :type random_id_1: str

            :param random_id_2: second identifiant généré alétoirement
            :type random_id_2: str

            :param nombre_de_jours: le nombre de jours entre la date du jour et le 1er janvier 2001
            :type nombre_de_jours: int

            :return: le jeton
            :rtype: str
        """

        # conversion du nombre de jours en base 36
        nombre_de_jours_b36 = int_to_base36(nombre_de_jours)

        # Génération d'un hash, limité à 20 caractères afin de raccourcir l'URL
        hash = salted_hmac(self.key_salt,
                           self._make_hash_value(random_id_1, random_id_2, nombre_de_jours),
                           secret=self.secret).hexdigest()[::2]

        # Définition de la valeur du jeton
        valeur_du_jeton = "{}-{}".format(nombre_de_jours_b36, hash)

        # Ajout du jeton ainsi créé à la base de données des jetons
        jeton = Jeton()
        jeton.valeur = valeur_du_jeton
        jeton.save()

        return valeur_du_jeton

    # ====================================================================
    def _make_hash_value(self, random_id_1, random_id_2, nombre_de_jours):
        """
            Méthode (privée) qui permet de créer une valeur de hash à partir de :

            - deux identifiants générés aléatoirements ;
            - du nombre de jours entre la date du jour et le 1er janvier 2001.

            :param random_id_1: premier identifiant généré alétoirement
            :type random_id_1: str

            :param random_id_2: second identifiant généré alétoirement
            :type random_id_2: str

            :param nombre_de_jours: le nombre de jours entre la date du jour et le 1er janvier 2001
            :type nombre_de_jours: int

            :return: une valeur de hash
            :rtype: str
        """

        return random_id_1 + random_id_2 + str(nombre_de_jours)

    # ==========================
    @staticmethod
    def _num_days(date_du_jour):
        """
            Méthode (privée) qui permet de récupérer le nombre de jours entre
            la date du jour et le 1er janvier 2001.

            :param date_du_jour: la date du jour
            :type date_du_jour: datetime.datetime

            :return: le nombre de jours entre la date du jour et le 1er janvier 2001
            :rtype: int
        """

        return (date_du_jour - datetime(2001, 1, 1)).days

    # ===========
    @staticmethod
    def _today():
        """
            Méthode (privée) qui permet de récupérer la date du jour.

            :return: la date du jour
            :rtype: datetime.datetime
        """

        return datetime.today()


# ==================================================================================================
# FONCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

default_token_generator = AccountCreationTokenGenerator()


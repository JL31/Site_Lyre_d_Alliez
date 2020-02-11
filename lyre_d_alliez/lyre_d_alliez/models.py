# coding: utf-8

"""
    Module de gestion des modèles
"""

# =================================================================================================
# PARAMETRES GLOBAUX
# =================================================================================================

__author__ = 'Julien LEPAIN'
__version__ = '1.0'
__maintainer__ = 'Julien LEPAIN'
__date__ = '10/2019'
__status__ = 'dev'


# ==================================================================================================
# IMPORTS
# ==================================================================================================

from django.db.models import OneToOneField, ImageField, TextField, CharField, BooleanField, CASCADE
from django.contrib.auth.models import User

from PIL import Image


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# =================
class Membre(User):
    """
        Classe qui décrit le modèle des membres
    """
    
    # liaison avec le modèle User
    user = OneToOneField(User, parent_link=True, unique=True, on_delete=CASCADE)
    
    avatar = ImageField(null=False, blank=False, upload_to="avatars/")
    description = TextField(null=True, blank=True, max_length=500)
    instruments = CharField(null=False, blank=False, max_length=255)

    chant = BooleanField(null=False, blank=True, default=False)
    est_membre = BooleanField(null=False, blank=True, default=False)
    est_membre_du_bureau = BooleanField(null=False, blank=True, default=False)
    est_le_chef = BooleanField(null=False, blank=True, default=False)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """
        
        verbose_name = "membre"
        ordering = ["avatar",
                    "username",
                    "first_name",
                    "email",
                    "description",
                    "instruments",
                    "chant",
                    "est_membre",
                    "est_membre_du_bureau",
                    "est_le_chef"
                   ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """
        
        return self.username

    # =============
    def save(self):
        """
            Permet d'enregister le logo dans un format différent de celui d'origine
            Nécessite au préalable d'importer la classe Image depuis PIL (from PIL import Image)
        """

        if not self.avatar:

            return

        super(Membre, self).save()
        image = Image.open(self.avatar)
        size = (40, 40)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.avatar.path)

    # ================================
    def get_instruments_as_list(self):
        """
            Permet de retourner la liste des instrument

            :return: la liste des instruments
            :rtype: list[str]
        """

        liste_temporaire = self.instruments.replace('[', '').replace(']', '')
        liste_temporaire = liste_temporaire.split(',')
        liste_temporaire = [ element.strip() for element in liste_temporaire ]
        return liste_temporaire

    # =================================
    def get_nombre_d_instruments(self):
        """
            Permet de retourner le nombre d'instruments

            :return: le nombre d'instruments
            :rtype: int
        """

        liste_temporaire = self.get_instruments_as_list()
        return len(liste_temporaire)


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

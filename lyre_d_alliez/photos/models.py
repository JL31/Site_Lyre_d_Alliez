from django.db import models

# Create your models here.
# coding: utf-8

"""
    Module de gestion des modèles pour l'application "photos"
"""

# =================================================================================================
# PARAMETRES GLOBAUX
# =================================================================================================

__author__ = 'Julien LEPAIN'
__version__ = '1.0'
__maintainer__ = 'Julien LEPAIN'
__date__ = '12/2019'
__status__ = 'dev'


# ==================================================================================================
# IMPORTS
# ==================================================================================================

from django.db import models


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ========================
class Photo(models.Model):
    """
        Classe qui décrit le modèle des photos
    """

    nom_du_fichier = models.CharField(null=False, blank=False, max_length=250)
    fichier = models.ImageField(null=False, blank=False, upload_to="photos/")

    nom_de_l_evenement = models.CharField(null=False, blank=False, max_length=250)
    date_de_l_evenement = models.DateField(null=False, blank=False)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        verbose_name = "photo"
        ordering = ["nom_du_fichier",
                    "fichier",
                    "nom_de_l_evenement",
                    "date_de_l_evenement"
                    ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.nom_du_fichier


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

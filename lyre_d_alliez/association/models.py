from django.db import models

# Create your models here.
# coding: utf-8

"""
    Module de gestion des modèles pour l'application "association"
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

from PIL import Image


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ==================================
class ArticleDePresse(models.Model):
    """
        Classe qui décrit le modèle des articles de presse
    """

    titre = models.CharField(null=False, blank=False, max_length=250)
    description = models.TextField(null=False, blank=False, max_length=1000)
    lien_vers_l_article = models.URLField(null=False, blank=False, max_length=750)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "article_de_presse"
        verbose_name = "article_de_presse"
        ordering = ["titre",
                    "description",
                    "lien_vers_l_article"
                    ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.titre


# ==========================
class Soutien(models.Model):
    """
        Classe qui décrit le modèle des soutiens
    """

    nom = models.CharField(null=False, blank=False, max_length=250)
    fichier = models.ImageField(null=False, blank=False, upload_to="logos/")
    site_internet = models.URLField(null=True, blank=True, max_length=750)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "soutien"
        verbose_name = "soutien"
        ordering = ["nom",
                    "fichier",
                    "site_internet"
                    ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.nom

    # =============
    def save(self):
        """
            Permet d'enregister le logo dans un format différent de celui d'origine
            Nécessite au préalable d'importer la classe Image depuis PIL (from PIL import Image)
        """

        if not self.fichier:

            return

        super(Soutien, self).save()
        image = Image.open(self.fichier)
        size = (150, 150)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.fichier.path)


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

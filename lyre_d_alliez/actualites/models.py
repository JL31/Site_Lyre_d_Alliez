# coding: utf-8

"""
    Module de gestion des modèles pour l'application "actualites"
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

from django.db import models
from django.utils import timezone

from lyre_d_alliez.models import Membre


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ============================
class Evenement(models.Model):
    """
        Classe qui décrit le modèle des évènements
    """

    nom = models.CharField(null=False, blank=False, max_length=255)
    lieu = models.CharField(null=False, blank=False, max_length=255)
    date = models.DateField(null=False, blank=False)
    programme = models.TextField(null=False, blank=False, max_length=1500)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "evenement"
        verbose_name = "evenement"
        ordering = ["nom",
                    "lieu",
                    "date",
                    "programme"
                   ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.nom


# =============================
class Abonnement(models.Model):
    """
        Classe qui décrit le modèle des abonnements
    """

    adresse_mail_abonne = models.EmailField(null=False, blank=False, max_length=255)
    date_de_l_alerte = models.DateField(null=False, blank=False)
    evenement = models.ForeignKey(Evenement, on_delete=models.SET_NULL, null=True, related_name="abonnement_evenement")

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "abonnement"
        verbose_name = "abonnement"
        ordering = ["adresse_mail_abonne",
                    "date_de_l_alerte",
                    "evenement"]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.adresse_mail_abonne


# ==========================
class Article(models.Model):
    """
        Classe qui décrit le modèle des articles
    """

    fichier = models.ImageField(null=False, blank=False, upload_to="images_articles/")
    titre = models.CharField(null=False, blank=False, max_length=250)
    description = models.TextField(null=False, blank=False, max_length=5000)
    date = models.DateField(default=timezone.now)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "article"
        verbose_name = "article"
        ordering = ["fichier",
                    "titre",
                    "description",
                    "date"
                   ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.titre


# ==============================
class Commentaire(models.Model):
    """
        Classe qui décrit le modèle des commentaires
    """

    texte = models.TextField(null=True, blank=False, max_length=5000)
    date = models.DateTimeField(default=timezone.now)
    articles = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="commentaire_articles")
    redacteur = models.ForeignKey(Membre, on_delete=models.CASCADE, null=True, related_name="commentaire_redacteur")

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        db_table = "commentaire"
        verbose_name = "commentaire"
        ordering = ["texte",
                    "date",
                    "articles",
                    "redacteur"
                    ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.texte


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

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

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    user = models.OneToOneField(User, parent_link=True, unique=True, on_delete=models.CASCADE)
    
    avatar = models.ImageField(null=False, blank=False, upload_to="avatars/")
    description = models.TextField(null=True, blank=True, max_length=500)
    instruments = models.CharField(null=False, blank=False, max_length=255)

    chant = models.BooleanField(null=False, blank=True, default=False)
    est_membre = models.BooleanField(null=False, blank=True, default=False)
    est_membre_du_bureau = models.BooleanField(null=False, blank=True, default=False)
    est_le_chef = models.BooleanField(null=False, blank=True, default=False)

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
            Permet d'enregister la photo dans un format différent que son format d'origine
            Nécessite au préalable d'importer la classe Image depuis PIL (from PIL import Image)
        """

        if not self.avatar:

            return

        super(Membre, self).save()
        image = Image.open(self.avatar)
        size = (40, 40)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.avatar.path)


# =============================
class Abonnement(models.Model):
    """
        Classe qui décrit le modèle des abonnements
    """

    adresse_mail_abonne = models.EmailField(null=False, blank=False, max_length=255)
    date_de_l_alerte = models.DateField(null=False, blank=False)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        verbose_name = "abonnement"
        ordering = ["adresse_mail_abonne",
                    "date_de_l_alerte"]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.adresse_mail_abonne


# ============================
class Evenement(models.Model):
    """
        Classe qui décrit le modèle des évènements
    """

    nom = models.CharField(null=False, blank=False, max_length=255)
    lieu = models.CharField(null=False, blank=False, max_length=255)
    date = models.DateField(null=False, blank=False)
    abonnements = models.ManyToManyField(Abonnement)
    # ==> à modifier en ForeignKey ?
    # ==> la Foreign Key sera sur le modèle Abonnement

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        verbose_name = "evenement"
        ordering = ["nom",
                    "lieu",
                    "date"
                   ]

    # ================
    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """

        return self.nom


# ==========================
class Article(models.Model):
    """
        Classe qui décrit le modèle des articles
    """

    image = models.ImageField(null=False, blank=False, upload_to="images_articles/")
    titre = models.CharField(null=False, blank=False, max_length=250)
    description = models.TextField(null=False, blank=False, max_length=5000)
    date = models.DateField(default=timezone.now)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

        verbose_name = "article"
        ordering = ["image",
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
    date = models.DateTimeField(default=timezone.now())
    articles = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    redacteur = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

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


# ==================================
class ArticleDePresse(models.Model):
    """
        Classe qui décrit le modèle des articles de presse
    """

    titre = models.CharField(null=False, blank=False, max_length=250)
    description = models.TextField(null=False, blank=False, max_length=1000)
    lien_vers_l_article = models.CharField(null=False, blank=False, max_length=750)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """

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


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

# coding: utf-8

"""
    Module de gestion de l'administration du site
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

from django.contrib import admin
from .models import Membre, Evenement, Abonnement, Article, Commentaire


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ==================================
class MembreAdmin(admin.ModelAdmin):
    """
        Classe qui permet la gestion de l'administration des membres
    """
    
    # Configuration de la liste d'articles
    list_display = ("username",
                    "first_name",
                    "email",
                    "instruments",
                    "chant",
                    "est_membre",
                    "est_membre_du_bureau",
                    "est_le_chef")
    
    list_filter = ("username",
                   "first_name",
                   "email",
                   "instruments",
                   "chant")
    
    date_hierarchy = "date_joined"
    
    ordering = ("date_joined", )
    
    search_fields = ("username",
                     "first_name",
                     "email",
                     "instruments",
                     "chant")
                     
    # Configuration du formulaire d'édition
    fieldsets = (("Propriétés du modèle User", {'fields': ("groups", 
                                                           "user_permissions",
                                                           "date_joined")}),
                 ("Propriétés du modèle Membre", {'fields': ("avatar", 
                                                             "username",
                                                             "first_name",
                                                             "email",
                                                             "description",
                                                             "instruments",
                                                             "chant",
                                                             "est_membre",
                                                             "est_membre_du_bureau",
                                                             "est_le_chef")}),
                 )


# =====================================
class EvenementAdmin(admin.ModelAdmin):
    """
        Classe qui permet la gestion de l'administration des membres
    """

    ### renommer en EvenementAdmin (sans le 's's à la fin) ?
    ###     ==> à impacter partout

    # Configuration de la liste d'articles
    list_display = ("nom",
                    "lieu",
                    "date")

    list_filter = ("nom",
                   "lieu",
                   "date")

    date_hierarchy = "date"

    ordering = ("date",)

    search_fields = ("nom",
                     "lieu",
                     "date")


# ======================================
class AbonnementAdmin(admin.ModelAdmin):
    """
        Classe qui permet la gestion de l'administration des abonnements
    """

    # Configuration de la liste d'articles
    list_display = ("adresse_mail_abonne",
                    "date_de_l_alerte")

    list_filter = ("adresse_mail_abonne",
                    "date_de_l_alerte")

    date_hierarchy = "date_de_l_alerte"

    ordering = ("date_de_l_alerte",)

    search_fields = ("adresse_mail_abonne",
                    "date_de_l_alerte")


# ===================================
class ArticleAdmin(admin.ModelAdmin):
    """
        Classe qui permet la gestion de l'administration des articles
    """

    # Configuration de la liste d'articles
    list_display = ("titre",
                    "date")

    list_filter = ("titre",
                   "date")

    date_hierarchy = "date"

    ordering = ("date",)

    search_fields = ("titre",
                     "date")


# =======================================
class CommentaireAdmin(admin.ModelAdmin):
    """
        Classe qui permet la gestion de l'administration des commentaires
    """

    # Configuration de la liste d'articles
    list_display = ("texte",
                    "date",
                    "articles")

    list_filter = ("texte",
                   "date",
                   "articles")

    date_hierarchy = "date"

    ordering = ("-date",)

    search_fields = ("texte",
                     "date",
                     "articles")

# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

admin.site.register(Membre, MembreAdmin)
admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Abonnement, AbonnementAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)

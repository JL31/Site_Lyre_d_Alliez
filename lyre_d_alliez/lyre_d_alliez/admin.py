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
from .models import Membre


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


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

admin.site.register(Membre, MembreAdmin)

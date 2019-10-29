# coding: utf-8

"""
    Module de gestion des formulaires
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

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Membre


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

# =================================
class MembreForm(UserCreationForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouveau membre
    """
    
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """
        
        model = Membre
        fields = ("avatar", "username", "first_name", "email", "description", "instrument", "chant")

    # ===============
    def clean(self):
        """
            Surcharge de la méthode clean
            
            :return: les données nettoyées
            :rtype: dict
        """
        
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(username=username).exists():
            
            message_d_erreur = "Un autre membre possède déjà ce nom d'utilisateur, merci d'en indiquer un autre."
            raise ValidationError(message_d_erreur)
            
        elif User.objects.filter(email=email).exists():
            
            message_d_erreur = "Un autre membre possède déjà cette adresse email, merci d'en indiquer une autre."
            raise ValidationError(message_d_erreur)
            
        return self.cleaned_data


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

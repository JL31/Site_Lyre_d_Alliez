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
from .models import Membre, Evenement, Abonnement, Article
from django.forms import MultipleChoiceField, ModelForm, EmailField, DateField, TextInput, DateInput
# from bootstrap_modal_forms.forms import BSModalForm


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

LISTE_DES_INSTRUMENTS = (('clarinette si b', 'clarinette si b'),
                         ('clarinette basse', 'clarinette basse'),
                         ('flute traversiere', 'flute traversière'),
                         ('flute traversiere basse', 'flute traversière basse'),
                         ('piccolo', 'piccolo'),
                         ('xylophone_marimba', 'xylophone / marimba'),
                         ('piano', 'piano'),
                         ('saxophone soprano', 'saxophone soprano'),
                         ('saxophone alto', 'saxophone alto'),
                         ('saxophone tenor', 'saxophone ténor'),
                         ('saxophone baryton', 'saxophone baryton'),
                         ('saxophone basse', 'saxophone basse'),
                         ('trombone', 'trombone'),
                         ('trombone basse', 'trombone basse'),
                         ('euphonium', 'euphonium'),
                         ('tuba', 'tuba'),
                         ('guitare seche', 'guitare sèche'),
                         ('guitare electrique', 'guitare électrique'),
                         ('guitare acoustique', 'guitare acoustique'),
                         ('mandoline', 'mandoline'),
                         ('guitare basse', 'guitare basse'),
                         ('trompette', 'trompette'),
                         ('batterie', 'batterie')
                        )

# ==================================================================================================
# CLASSES
# ==================================================================================================

# =================================
class MembreForm(UserCreationForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouveau membre
    """

    instruments = MultipleChoiceField(choices=LISTE_DES_INSTRUMENTS)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """
        
        model = Membre
        fields = ("avatar", "username", "first_name", "email", "description", "instruments", "chant")

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


# =============================
class EvenementForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel évènement
    """

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Evenement
        fields = ("nom", "lieu", "date")


# =======================================
# class AbonnementEvenementForm(BSModalForm):
class AbonnementEvenementForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour l'abonnement à un évènement
    """

    adresse_email = EmailField(label="Indiquez votre adresse email", required=True)
    confirmation_adresse_email = EmailField(label="Confirmez votre adresse email", required=True)
    date_envoi_alerte = DateField(label="Date d'envoi de l'alerte")

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Abonnement

        fields = ("adresse_email",
                  "confirmation_adresse_email",
                  "date_envoi_alerte")

        widgets = {'adresse_email': TextInput(attrs={'type': 'email', 'placeholder': 'exemple: jean.dupont@test.fr'}),
                   'confirmation_adresse_email': TextInput(attrs={'type': 'email', 'placeholder': 'exemple: jean.dupont@test.fr'}),
                   'date_envoi_alerte': DateInput(format='%d-%m-%Y',
                                                  attrs={'class': 'myDateClass', 'placeholder': 'Choisissez une date', 'required': True})
                  }

    # ===============
    def clean(self):
        """
            Surcharge de la méthode clean

            :return: les données nettoyées
            :rtype: dict
        """

        adresse_email = self.cleaned_data.get("adresse_email")
        confirmation_adresse_email = self.cleaned_data.get("confirmation_adresse_email")

        if adresse_email != confirmation_adresse_email:

            message_d_erreur = "Les deux adresses mail ne sont pas identiques, merci de corriger votre saisie"
            raise ValidationError(message_d_erreur)

        return self.cleaned_data


# ===========================
class ArticleForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel article
    """

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Article
        fields = ("image", "titre", "description")


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

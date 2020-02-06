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

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from lyre_d_alliez.models import Membre

from django.forms import MultipleChoiceField


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

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur
        """

        super(MembreForm, self).__init__(*args, **kwargs)
        self.fields['instruments'].label = "Instruments (choisissez-en un ou plusieurs)"
        self.fields['chant'].label = "Chant (cochez la case si vous chantez)"

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


# =====================================
class UpdateMembreForm(UserChangeForm):
    """
        Classe qui permet la création d'un formulaire pour la mise-à-jour des données personnelles d'un membre
    """

    instruments = MultipleChoiceField(choices=LISTE_DES_INSTRUMENTS)

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur
        """

        super(UpdateMembreForm, self).__init__(*args, **kwargs)
        self.fields["instruments"].label = "Instruments (choisissez-en un ou plusieurs)"
        self.fields["chant"].label = "Chant (cochez la case si vous chantez)"
        del self.fields["password"]

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Membre
        fields = ("avatar", "username", "first_name", "email", "description", "instruments", "chant")


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

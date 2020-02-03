# coding: utf-8

"""
    Module de gestion des formulaires de l'application "acces"
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

from django.forms import Form, CharField, PasswordInput, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ===============================
class AuthentificationForm(Form):
    """
        Classe qui permet la création d'un formulaire pour l'authentification
    """

    login = CharField(required=True, max_length=250, label="Nom d'utilisateur")
    mot_de_passe = CharField(required=True, widget=PasswordInput())

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        fields = ("login", "mot_de_passe")


# ===================================
class ConfirmPasswordForm(ModelForm):
    """
        Classe qui permet la confirmation du mot de passe d'un membre
    """

    confirmer_le_mot_de_passe = CharField(widget=PasswordInput())

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = User
        fields = ("confirmer_le_mot_de_passe",)

    # ==============
    def clean(self):
        """
            Méthode qui permet de vérifier que le mot de passe indiqué par l'utilisateur est bien celui associé à son compte
        """

        cleaned_data = super(ConfirmPasswordForm, self).clean()

        confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

        if not check_password(confirmer_le_mot_de_passe, self.instance.password):

            self.add_error("confirmer_le_mot_de_passe", "Erreur dans le mot de passe")


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

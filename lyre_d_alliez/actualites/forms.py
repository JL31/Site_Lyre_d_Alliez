# coding: utf-8

"""
    Module de gestion des formulaires de l'application "actualites"
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

from actualites.models import Commentaire

from lyre_d_alliez.settings import DATE_INPUTS_FORMATS

from actualites.models import Evenement, Article, Abonnement

from django.forms import ModelForm, EmailField, DateField, TextInput, DateInput, Textarea


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

# =============================
class EvenementForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel évènement
    """

    date = DateField(required=True, input_formats=DATE_INPUTS_FORMATS)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Evenement
        fields = ("nom", "lieu", "date", "programme")


# =======================================
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

        # # ==============
        # def clean(self):
        #     """
        #         Surcharge de la méthode clean
        #
        #         :return: les données nettoyées
        #         :rtype: dict
        #     """
        #
        #     adresse_email = self.cleaned_data.get("adresse_email")
        #     confirmation_adresse_email = self.cleaned_data.get("confirmation_adresse_email")
        #
        #     if adresse_email != confirmation_adresse_email:
        #
        #         message_d_erreur = "Les deux adresses mail ne sont pas identiques, merci de corriger votre saisie"
        #         raise ValidationError(message_d_erreur)
        #
        #     return self.cleaned_data


# ===========================
class ArticleForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel article
    """

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les lignes suivantes permettent de modifier les label d'un champ dans la page
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["fichier"].label = "Image"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Article
        fields = ("fichier", "titre", "description")


# ===============================
class CommentaireForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouveau commentaire
    """

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les deux lignes suivantes permettent de ne pas afficher le label du champ "texte" dans la page (en réalité le label est vide)
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["texte"].label = ""

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Commentaire
        fields = ("texte", )
        widgets = {"texte": Textarea(attrs={"placeholder": "Rédigez votre commentaire ici"}),}


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

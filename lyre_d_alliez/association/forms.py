# coding: utf-8

"""
    Module de gestion des formulaires de l'application "association"
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

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField, Textarea

from association.models import ArticleDePresse, Soutien


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# ===================================
class ArticleDepresseForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel article de presse
    """

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les deux lignes suivantes permettent de modifier le label du champ "lien_vers_l_article" dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["lien_vers_l_article"].label = "Lien vers l'article"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = ArticleDePresse
        fields = ("titre", "description", "lien_vers_l_article")


# ===========================
class SoutienForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'un nouvel article de presse
    """

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les lignes suivantes permettent de modifier les label d'un champ dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["site_internet"].label = "Site internet"
        self.fields["fichier"].label = "Logo"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Soutien
        fields = ("nom", "fichier", "site_internet")


# ====================================
class DemandeDevenirSoutienForm(Form):
    """
        Classe qui permet la création d'un formulaire pour renseigner les champs d'une demande pour devenir soutien de l'asso
    """

    telephone_regexp = RegexValidator(regex=r"^0\d[ .]?(\d{2}[ .]?){4}$", message=("Le numéro de téléphone doit avoir l'un des formats suivant :\n"
                                                                                   "- 00.11.22.33.44,\n"
                                                                                   "- 0011223344,\n"
                                                                                   "- 00 11 22 33 44"))

    nom = CharField(required=True, max_length=250)
    prenom = CharField(required=True, max_length=250)
    societe = CharField(required=False, max_length=250)
    adresse_email = EmailField(required=False, max_length=255)
    numero_de_telephone = CharField(required=False, max_length=14, validators=[telephone_regexp])
    message = CharField(widget=Textarea, required=True, max_length=5000)

    # ==============
    def clean(self):
        """
            Surcharge de la méthode clean

            :return: les données nettoyées
            :rtype: dict
        """

        adresse_email = self.cleaned_data.get("adresse_email")
        numero_de_telephone = self.cleaned_data.get("numero_de_telephone")

        if (adresse_email is None or adresse_email == "") and (numero_de_telephone is None or numero_de_telephone == ""):

            message_d_erreur = "Veuillez saisir soit une adresse email soit un numéro de téléphone"
            raise ValidationError(message_d_erreur)

        return self.cleaned_data


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

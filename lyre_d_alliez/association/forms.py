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

from django.forms import ModelForm

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


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

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
__date__ = '11/2019'
__status__ = 'dev'


# ==================================================================================================
# IMPORTS
# ==================================================================================================

from actualites.models import Commentaire
from django.forms import ModelForm, Textarea


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

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

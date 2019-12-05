# coding: utf-8

"""
    Module de gestion des formulaires de l'application "videos"
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

from django.forms import ModelForm, DateField
from django.forms import FileField, ClearableFileInput

from videos.models import Video

from lyre_d_alliez.settings import DATE_INPUTS_FORMATS

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# =========================
class VideoForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour uploader une(des) vidéo(s)
    """

    fichier = FileField(widget=ClearableFileInput(attrs={"multiple": True}))
    date_de_l_evenement = DateField(required=True, input_formats=DATE_INPUTS_FORMATS)   # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les lignes suivantes permettent de modifier les label d'un champ dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["nom_de_l_evenement"].label = "Nom de l'évènement"
        self.fields["date_de_l_evenement"].label = "Date de l'évènement"    # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm
        self.fields["poster_de_la_video"].label = "Poster de la vidéo"      # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm
        self.fields["fichier"].label = "Vidéo(s)"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Video
        fields = ("fichier", "poster_de_la_video", "nom_de_l_evenement", "date_de_l_evenement")


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

# coding: utf-8

"""
    Module de gestion des formulaires de l'application "les outils du chef"
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

from actualites.models import Evenement, Article
from association.models import ArticleDePresse, Soutien
from photos.models import Photo
from videos.models import Video

from lyre_d_alliez.settings import DATE_INPUTS_FORMATS

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# =============================
class EvenementForm(ModelForm):
    """
        Classe qui permet la création
        d'un formulaire pour renseigner les champs d'un nouvel évènement
    """

    date = DateField(required=True, input_formats=DATE_INPUTS_FORMATS)

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Evenement
        fields = ("nom", "lieu", "date", "programme")


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


# =========================
class PhotoForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour uploader une(des) photo(s)
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
        self.fields["fichier"].label = "Photo(s)"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Photo
        fields = ("fichier", "nom_de_l_evenement", "date_de_l_evenement")


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

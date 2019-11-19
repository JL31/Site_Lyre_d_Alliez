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
from django.core.validators import RegexValidator
from django.forms import Form, CharField, FileField, ClearableFileInput

from .models import Membre, Evenement, Abonnement, Article, Commentaire, ArticleDePresse, Soutien, Photo, Video
from django.forms import MultipleChoiceField, ModelForm, EmailField, DateField, TextInput, DateInput, Textarea

from .settings import DATE_INPUTS_FORMATS


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

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Article
        fields = ("image", "titre", "description")


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

        # Les deux lignes suivantes permettent de ne pas afficher le label du champ "texte" dans la page (en réalité le lable est vide)
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

        # Les deux lignes suivantes permettent de modifier le label du champ "site_internet" dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["site_internet"].label = "Site internet"

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Soutien
        fields = ("nom", "logo", "site_internet")


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


# =========================
class PhotoForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour uploader une(des) photo(s)
    """

    photo = FileField(widget=ClearableFileInput(attrs={"multiple": True}))
    date_de_l_evenement = DateField(required=True, input_formats=DATE_INPUTS_FORMATS)   # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les lignes suivantes permettent de modifier les labels de certains champs dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["nom_de_l_evenement"].label = "Nom de l'évènement"
        self.fields["date_de_l_evenement"].label = "Date de l'évènement"    # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Photo
        fields = ("photo", "nom_de_l_evenement", "date_de_l_evenement")


# =========================
class VideoForm(ModelForm):
    """
        Classe qui permet la création d'un formulaire pour uploader une(des) vidéo(s)
    """

    video = FileField(widget=ClearableFileInput(attrs={"multiple": True}))
    date_de_l_evenement = DateField(required=True, input_formats=DATE_INPUTS_FORMATS)   # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm

    # ==================================
    def __init__(self, *args, **kwargs):
        """
            Constructeur de la classe
        """

        # Les lignes suivantes permettent de modifier les labels de certains champs dans la page
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["nom_de_l_evenement"].label = "Nom de l'évènement"
        self.fields["date_de_l_evenement"].label = "Date de l'évènement"    # utiliser plutôt l'attribut label comme pour AbonnementEvenementForm

    # =========
    class Meta:
        """
            Configuration/définition des options de metadonnées du formulaire
        """

        model = Video
        fields = ("video", "nom_de_l_evenement", "date_de_l_evenement")


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

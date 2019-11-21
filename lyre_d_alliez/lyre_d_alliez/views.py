# coding: utf-8

"""
    Module de gestion des vues
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

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.core.mail import mail_admins, send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

from .forms import MembreForm, LISTE_DES_INSTRUMENTS, EvenementForm, AbonnementEvenementForm, ArticleForm, CommentaireForm, ArticleDepresseForm, SoutienForm, DemandeDevenirSoutienForm, PhotoForm, VideoForm
from .models import Membre, Evenement, Abonnement, Article, Commentaire, ArticleDePresse, Soutien, Photo, Video

from .secret_data import ADMINS, MOT_DE_PASSE

from collections import OrderedDict
from datetime import datetime
from locale import setlocale, LC_TIME
from smtplib import SMTPException


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================


# ==============================
def personne_autorisee(request):
    """
        Fonction pour vérifier si le visiteur est autorisée à accéder à certaines pages

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: un booléen indiquant :

                 - True si le visiteur est :

                   + un membre ;
                   + un membre du bureau ;
                   + le chef.

                 - False sinon
        :rtype: bool
    """

    try:

        return request.membre.est_membre or request.membre.est_membre_du_bureau or request.membre.est_le_chef

    except AttributeError:
        "La gestion de cette erreur est nécessaire car les instances d'objet 'AnonymousUser' ne possèdent pas l'attribut 'membre'"

        return False


# ============================================
def envoi_mail_admin_nouveau_membre(**kwargs):
    """
        Fonction qui permet d'envoyer un mail à l'admin pour l'informer qu'un nouveau membre a été créé
    """

    sujet = " Inscription d'un nouveau membre"
    message = ("Une personne vient de remplir le formulaire d'inscription à la zone des membres.\n\n"
               "Merci de vérifier les informations renseignées et de lui attribuer les accès en tant que : \n\n"
               "- membre ;\n"
               "- membre du bureau ;\n"
               "- chef.")
    expediteur = ADMINS[0][1]
    destinataire = [ADMINS[0][1]]

    utilisateur = ADMINS[0][1]
    mot_de_passe = MOT_DE_PASSE

    # mail_admins(sujet, message)
    try:

        send_mail(sujet, message, expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

    except SMTPException:

        msg = "Problème lors de l'envoi de mail après la création d'un compte membre"
        raise SMTPException(msg)


# =================================
@receiver(post_save, sender=Membre)
def envoi_mail(sender, **kwargs):
    """
        Fonction qui permet d'envoyer un mail

        :param sender: l'instance du modèle Soutien qui est en cours de suppression
        :type sender: lyre_d_alliez.models.Soutien
    """

    sujet = " Inscription d'un nouveau membre"
    message = ("Une personne vient de remplir le formulaire d'inscription à la zone des membres.\n\n"
               "Merci de vérifier les informations renseignées et de lui attribuer les accès en tant que : \n\n"
               "- membre ;\n"
               "- membre du bureau ;\n"
               "- chef.")
    expediteur = ADMINS[0][1]
    destinataire = [ADMINS[0][1]]
    utilisateur = ADMINS[0][1]
    mot_de_passe = MOT_DE_PASSE

    try:

        send_mail(sujet, message, expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

    except SMTPException:

        msg = "Problème lors de l'envoi de mail après la création d'un compte membre"
        raise SMTPException(msg)


# ==========================================================
@receiver(post_delete, sender=Soutien)
def supprimer_logo_d_un_soutien(sender, instance, **kwargs):
    """
        Fonction qui permet de supprimer, sur le serveur, le logo d'un soutien dans le cas où ce dernier serait supprimé

        :param sender: expéditeur qui va envoyer le signal
        :type sender: django.db.models.base.ModelBase

        :param instance: l'instance du modèle Soutien qui est en cours de suppression
        :type instance: lyre_d_alliez.models.Soutien
    """

    instance.logo.delete(False)


# ===================================
def envoi_mail_bis(dico_des_donnees):
    """
        Fonction qui permet d'envoyer un mail

        :param dico_des_donnees: liste des paramètres nommés (sujet, message)
        ::type dico_des_donnees: dict
    """

    expediteur = ADMINS[0][1]
    destinataire = [ADMINS[0][1]]
    utilisateur = ADMINS[0][1]
    mot_de_passe = MOT_DE_PASSE

    try:

        send_mail(dico_des_donnees["sujet"], dico_des_donnees["message"], expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

    except SMTPException:

        msg = dico_des_donnees["message_d_erreur"]
        raise SMTPException(msg)


# ====================================
def acces_restreints_au_chef(request):
    """
        Fonction pour vérifier si le visiteur est le chef

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: un booléen indiquant :
                 - True si le visiteur est le chef
                 - False sinon
        :rtype: bool
    """

    try:

        return request.membre.est_le_chef

    except AttributeError:
        "La gestion de cette erreur est nécessaire car les instances d'objet 'AnonymousUser' ne possèdent pas l'attribut 'membre'"

        return False


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

decorators = [login_required, user_passes_test(acces_restreints_au_chef)]


# ==================================================================================================
# CLASSES
# ==================================================================================================


# =============================================
@method_decorator(decorators, name='dispatch')
class PhotoView(SuccessMessageMixin, FormView):
    """
        Classe générique permettant la gestion du chargement de plusieurs photos
    """

    form_class = PhotoForm
    template_name = "AjoutPhotosForm.html"
    success_url = reverse_lazy("accueil")
    success_message = "La(les) photo(s) a(ont) bien été ajoutée(s)"

    # =======================================
    def post(self, request, *args, **kwargs):
        """
            Surcharge de la méthode 'post' de la classe 'ProcessFormView':

            Gère les requête POST : instantie une instance 'form' avec les
            variables POST passées en argument puis vérifie si c'est valide

            :param request: instance de HttpRequest
            :type request: django.core.handlers.wsgi.WSGIRequest

            :param args: arguments non nommés
            :type args: List

            :param kwargs: arguments nommés
            :type kwargs: dict

            :return: instance de HttpResponse
            :rtype: django.http.response.HttpResponseRedirect
        """

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist("photo")

        if form.is_valid():

            for file in files:

                photo_en_cours = Photo()
                photo_en_cours.photo = file
                photo_en_cours.nom_de_la_photo = file.name
                photo_en_cours.nom_de_l_evenement = form.cleaned_data.get("nom_de_l_evenement")
                photo_en_cours.date_de_l_evenement = form.cleaned_data.get("date_de_l_evenement")
                photo_en_cours.save()

            return self.form_valid(form)

        else:

            return self.form_invalid(form)


# =============================================
@method_decorator(decorators, name='dispatch')
class VideoView(SuccessMessageMixin, FormView):
    """
        Classe générique permettant la gestion du chargement de plusieurs vidéos
    """

    form_class = VideoForm
    template_name = "AjoutVideoForm.html"
    success_url = reverse_lazy("accueil")
    success_message = "La(les) vidéo(s) a(ont) bien été ajoutée(s)"

    # =======================================
    def post(self, request, *args, **kwargs):
        """
            Surcharge de la méthode 'post' de la classe 'ProcessFormView':

            Gère les requête POST : instantie une instance 'form' avec les
            variables POST passées en argument puis vérifie si c'est valide

            :param request: instance de HttpRequest
            :type request: django.core.handlers.wsgi.WSGIRequest

            :param args: arguments non nommés
            :type args: List

            :param kwargs: arguments nommés
            :type kwargs: dict

            :return: instance de HttpResponse
            :rtype: django.http.response.HttpResponseRedirect
        """

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist("video")

        if form.is_valid():

            for file in files:

                video_en_cours = Video()
                video_en_cours.video = file
                video_en_cours.nom_de_la_video = file.name
                video_en_cours.nom_de_l_evenement = form.cleaned_data.get("nom_de_l_evenement")
                video_en_cours.date_de_l_evenement = form.cleaned_data.get("date_de_l_evenement")
                video_en_cours.save()

            return self.form_valid(form)

        else:

            return self.form_invalid(form)


# ==================================================================================================
# VUES
# ==================================================================================================


# ===================
def accueil(request):
    """
        Vue de la page d'accueil

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "base_etendue.html")


# ======================
def actualites(request):
    """
        Vue pour les actualités

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "sous_menu_actualites.html")


# =======================
def association(request):
    """
        Vue pour l'association

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "sous_menu_association.html")


# # ===================================
# @login_required
# @user_passes_test(personne_autorisee)
# def zone_de_partage(request):
#     """
#         Vue pour la zone de partage
#
#         :param request: instance de HttpRequest
#         :type request: django.core.handlers.wsgi.WSGIRequest
#
#         :return: instance de HttpResponse
#         :rtype: django.http.response.HttpResponse
#     """
#
#     return render(request, "sous_menu_zone_de_partage.html")


# ==================================
def creation_profil_membre(request):
    """
        Vue pour la création du profil d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    if request.method == "POST":

        form = MembreForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            msg = "Le profil a été crée avec succès, merci d'attendre l'email d'activation de votre compte"
            messages.info(request, msg)
            return HttpResponseRedirect(reverse("accueil"))

    else:

        form = MembreForm()

    return render(request, "MembreForm.html", {"form": form})


# ==========================
def acces_interdit(request):
    """
        Vue pour l'accès interdit à une page du site

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "acces_interdit.html")


# ========================
def les_pupitres(request):
    """
        Vue des pupitres

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_membres = Membre.objects.all()
    liste_des_instruments = ( instrument for instrument in LISTE_DES_INSTRUMENTS )

    dico_instrument_membres = OrderedDict()

    for instrument in liste_des_instruments:

        for membre in liste_des_membres:

            if instrument[0] in membre.instruments:
                dico_instrument_membres.setdefault(instrument[0], {"instrument": instrument[1], "membres": []})["membres"].append(membre)

    return render(request, "les_pupitres.html", {"dico_instrument_membres": dico_instrument_membres})


# ==================
def agenda(request):
    """
        Vue de l'agenda

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_evenements = Evenement.objects.all()

    return render(request, "agenda.html", {"liste_des_evenements": liste_des_evenements})


# # =========================================
# @login_required
# @user_passes_test(acces_restreints_au_chef)
# def creation_evenement(request):
#     """
#         Vue pour la création d'un évènement
#
#         :param request: instance de HttpRequest
#         :type request: django.core.handlers.wsgi.WSGIRequest
#
#         :return: instance de HttpResponse ou de HttpResponseRedirect
#         :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
#     """
#
#     if request.method == "POST":
#
#         form = EvenementForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             msg = "L'évènement a été crée avec succès"
#             messages.info(request, msg)
#             return HttpResponseRedirect(reverse("accueil"))
#
#     else:
#
#         form = EvenementForm()
#
#     return render(request, "EvenementForm.html", {"form": form})
# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def creation_evenement(request):
    """
        Vue pour la création d'un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Création d'un évènement"
    classe_pour_envoi_formulaire = "js-creation-evenement-creation-formulaire"
    titre_du_bouton_pour_validation = "Créer l'évènement"
    id_champ_date = "#id_date"
    formulaire = EvenementForm

    # Création du contexte
    donnees = {
               "url_pour_action": url_pour_action,
               "titre_du_formulaire": titre_du_formulaire,
               "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
               "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
               "id_champ_date": id_champ_date,
               "formulaire": formulaire
              }

    return creation_formulaire_outils_du_chef(request, donnees)


# =======================================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def creation_formulaire_outils_du_chef(request, donnees):
    """
        Vue qui permet d'afficher le formulaire demandé avec les données passées en argument

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param donnees: données issues de la vue appelant la vue
        :type donnees: dict

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    if request.method == "POST":

        form = donnees["formulaire"](request.POST)

        if form.is_valid():

            form.save()

            data["form_is_valid"] = True

            msg = "L'évènement a été crée avec succès"
            messages.info(request, msg)

        else:

            data["form_is_valid"] = False

    else:

        form = donnees["formulaire"]()

    context = {"form": form}
    context.update(donnees)
    del context["formulaire"]

    data["html_form"] = render_to_string("formulaire_outils_du_chef.html", context, request=request)

    return JsonResponse(data)


# ==============================================
def abonnement_evenement(request, id_evenement):
    """
        Vue pour la gestion d'un abonnement à un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param id_evenement: id de l'évènement
        :type id_evenement: str (int onverti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    id_evenement_int = int(id_evenement)

    if request.method == "POST":

        form = AbonnementEvenementForm(request.POST)

        if form.is_valid():

            evenement = Evenement.objects.filter(id=id_evenement_int)

            if len(evenement) > 1:

                # à améliorer
                msg = "Erreur --- vue abonnement_evenement --- filtre nom : plus d'une personne"
                raise ValueError(msg)

            else:

                # mettre en place un système pour éviter les doublons
                # quid si un même visiteur souhaite programmer deux alertes à la même date ?

                adresse_mail_abonne = form.cleaned_data.get("adresse_email")
                date_de_l_alerte = form.cleaned_data.get("date_envoi_alerte")

                setlocale(LC_TIME, "fr-FR")  # permet d'obtenir la date au format local (ici Fr)

                abonnement = Abonnement(adresse_mail_abonne=adresse_mail_abonne, date_de_l_alerte=date_de_l_alerte)
                abonnement.save()

                for obj in evenement:

                    abonnement.evenement = obj
                    abonnement.save()
                    msg = "Votre demande d'abonnement a bien été prise en compte. Vous recevrez un email pour vous alerter le {} à l'adresse suivante : {}".format(date_de_l_alerte.strftime("%A %d %B %Y"), adresse_mail_abonne)
                    messages.info(request, msg)

            data["form_is_valid"] = True

        else:

            data["form_is_valid"] = False

    else:

            form = AbonnementEvenementForm()

    context = {"form": form, "id_evenement": id_evenement}
    data["html_form"] = render_to_string("formulaire_abonnement_evenement.html", context, request=request)

    return JsonResponse(data)


# ===============================
def envoi_alerte_abonne(request):
    """
        Vue pour la gestion de l'envoi d'une alerte à un abonné concernant un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    liste_des_evenements = Evenement.objects.all()

    for evenement in liste_des_evenements:

        liste_des_abonnes = evenement.abonnements.all()

        for abonne in liste_des_abonnes:

            if abonne.date_de_l_alerte.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
                sujet = " Rappel "
                message = ("La Lyre d'Alliez vous rappelle que le {{ evenement.nom }} aura lieu à {{ evenement.lieu }} le {{ evenement.date }}<br />"
                           "Ceci est un message automatique envoyé à {{ abonne.adresse_mail_abonne }}")
                msg_erreur = "Problème lors de l'envoi d'une alerte mail à un abonné"

                envoi_mail(sujet=sujet, message=message, msg_erreur=msg_erreur)

    return HttpResponseRedirect(reverse("accueil"))


# ==================
def bureau(request):
    """
        Vue du bureau

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    chef = Membre.objects.filter(est_le_chef=True)

    if len(chef) > 1:

        # à améliorer
        msg = "Erreur --- vue bureau --- filtre est_le_chef : plus d'une personne"
        raise ValueError(msg)

    else:

        for obj in chef:
            chef = obj

    liste_des_membres_du_bureau = Membre.objects.filter(est_membre_du_bureau=True)

    return render(request, "bureau.html", {"chef": chef, "liste_des_membres_du_bureau": liste_des_membres_du_bureau})


# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def creation_article(request):
    """
        Vue du formulaire permettant la création d'un nouvel article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # if request.method == "POST":
    #
    #     form = ArticleForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         form.save()
    #         msg = "L'article a été crée avec succès"
    #         messages.info(request, msg)
    #         return HttpResponseRedirect(reverse("accueil"))
    #
    # else:
    #
    #     form = ArticleForm()
    #
    # return render(request, "ArticleForm.html", {"form": form})

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Création d'un article"
    classe_pour_envoi_formulaire = "js-creation-article-creation-formulaire"
    titre_du_bouton_pour_validation = "Créer l'article"
    id_champ_date = ""
    formulaire = ArticleForm

    # Création du contexte
    donnees = {
               "url_pour_action": url_pour_action,
               "titre_du_formulaire": titre_du_formulaire,
               "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
               "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
               "id_champ_date": id_champ_date,
               "formulaire": formulaire
              }

    return creation_formulaire_outils_du_chef(request, donnees)


# ==============================
def liste_des_articles(request):
    """
        Vue permettant de lister tous les articles créés

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_articles = Article.objects.order_by("-date")

    return render(request, "liste_des_articles.html", {"liste_des_articles": liste_des_articles})


# ================================================
def lire_article(request, reference_de_l_article):
    """
        Vue qui permet de lire un article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param reference_de_l_article: référence de l'article (sous forme d'id)
        :type reference_de_l_article: int

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # Récupération du contenu de l'article sélectionné
    # ------------------------------------------------

    article = Article.objects.filter(id=reference_de_l_article)

    # Récupération des commentaires associés à l'article sélectionné
    # --------------------------------------------------------------

    liste_des_commentaires = None

    if len(article) > 1:

        # à améliorer
        msg = "Erreur --- vue lire_article --- filtre id : plus d'un article"
        raise ValueError(msg)

    else:

        for obj in article:
            article = obj
            liste_des_commentaires = Commentaire.objects.filter(articles=obj).order_by("-date")

    # Gestion du formulaire permettant l'ajout d'un commentaire à l'article sélectionné
    # ---------------------------------------------------------------------------------

    if request.method == "POST":

        form = CommentaireForm(request.POST)

        if form.is_valid():

            commentaire = form.save(commit=False)
            commentaire.date = timezone.now()
            commentaire.articles = article
            commentaire.redacteur = request.user.membre
            commentaire.save()

            return HttpResponseRedirect(reverse("lire_article", kwargs={"reference_de_l_article": reference_de_l_article}))

    else:

        form = CommentaireForm()

    return render(request, "lecture_article.html", {"article": article, "liste_des_commentaires": liste_des_commentaires, "form": form})


# =========================================
@login_required
@user_passes_test(personne_autorisee)
def articles_de_presse(request):
    """
        Vue qui permet de lire un article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_articles_de_presse = ArticleDePresse.objects.all()

    return render(request, "articles_de_presse.html", {"liste_des_articles_de_presse": liste_des_articles_de_presse})


# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def creation_article_de_presse(request):
    """
        Vue du formulaire permettant la création d'un nouvel article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # if request.method == "POST":
    #
    #     form = ArticleDepresseForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         msg = "Le lien vers l'article de presse a bien été ajouté"
    #         messages.info(request, msg)
    #         return HttpResponseRedirect(reverse("accueil"))
    #
    # else:
    #
    #     form = ArticleDepresseForm()
    #
    # return render(request, "ArticleDePresseForm.html", {"form": form})

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Création d'un article de presse"
    classe_pour_envoi_formulaire = "js-creation-article-de-presse-creation-formulaire"
    titre_du_bouton_pour_validation = "Créer l'article de presse"
    id_champ_date = ""
    formulaire = ArticleDepresseForm

    # Création du contexte
    donnees = {
        "url_pour_action": url_pour_action,
        "titre_du_formulaire": titre_du_formulaire,
        "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
        "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
        "id_champ_date": id_champ_date,
        "formulaire": formulaire
    }

    return creation_formulaire_outils_du_chef(request, donnees)


# ====================
def soutiens(request):
    """
        Vue qui permet d'afficher les soutiens

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_soutiens = Soutien.objects.all()

    return render(request, "soutiens.html", {"liste_des_soutiens": liste_des_soutiens})


# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def creation_soutien(request):
    """
        Vue du formulaire permettant la création d'un nouveau soutien

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # if request.method == "POST":
    #
    #     form = SoutienForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         form.save()
    #         msg = "Le soutien a bien été ajouté"
    #         messages.info(request, msg)
    #         return HttpResponseRedirect(reverse("accueil"))
    #
    # else:
    #
    #     form = SoutienForm()
    #
    # return render(request, "SoutienForm.html", {"form": form})

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Création d'un soutien"
    classe_pour_envoi_formulaire = "js-creation-soutien-creation-formulaire"
    titre_du_bouton_pour_validation = "Créer le soutien"
    id_champ_date = ""
    formulaire = SoutienForm

    # Création du contexte
    donnees = {
        "url_pour_action": url_pour_action,
        "titre_du_formulaire": titre_du_formulaire,
        "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
        "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
        "id_champ_date": id_champ_date,
        "formulaire": formulaire
    }

    return creation_formulaire_outils_du_chef(request, donnees)


# ========================================
def demande_pour_devenir_soutien(request):
    """
        Vue du formulaire permettant la demande pour devenir un soutien de l'asso

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    if request.method == "POST":

        form = DemandeDevenirSoutienForm(request.POST)

        if form.is_valid():

            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            societe = form.cleaned_data["societe"]
            adresse_email = form.cleaned_data["adresse_email"]
            numero_de_telephone = form.cleaned_data["numero_de_telephone"]
            message = form.cleaned_data["message"]

            # définition du sujet du mail
            sujet = "Demande pour devenir soutien de l'asso"

            # définition des coordonnées de la personne qui envoie la demande de soutien
            # améliorable avec la version 3.6 et le formatted string literal
            coordonnees = ""

            if adresse_email != "" and numero_de_telephone == "":

                coordonnees = "adresse email : {}".format(adresse_email)

            elif adresse_email == "" and numero_de_telephone != "":

                coordonnees = "numéro de téléphone : {}".format(numero_de_telephone)

            elif adresse_email != "" and numero_de_telephone != "":

                coordonnees = "adresse email : {}\nnuméro de téléphone : {}".format(adresse_email, numero_de_telephone)

            # définition du début du message (selon si un nom de société a été renseigné ou non)
            if societe != "":

                debut_message = ("La société {} souhaite devenir soutien de l'association.\n"
                                 "La personne a contacter est {} {},").format(societe, prenom, nom)

            else:

                debut_message = "{} {} souhaite devenir soutien de l'association,".format(prenom, nom)

            # définition du message à envoyer
            message_a_envoyer = ("{} ses coordonnées sont :\n\n"
                                 "{}\n\n"
                                 "Voici son message :\n\n"
                                 "{}").format(debut_message, coordonnees, message)

            message_d_erreur = "Problème lors de l'envoi d'un mail de demande pour devenir soutien de l'asso"

            # envoi d'un mail contenant les données définies précédemment
            dico_des_donnees = {
                                "sujet": sujet,
                                "message": message_a_envoyer,
                                "message_d_erreur": message_d_erreur
                               }
            envoi_mail_bis(dico_des_donnees)

            msg = "Votre demande a bien été envoyée"
            messages.info(request, msg)
            return HttpResponseRedirect(reverse("soutiens"))

    else:

        form = DemandeDevenirSoutienForm()

    return render(request, "DemandeDevenirSoutienForm.html", {"form": form})


# ===================================
def historique_des_concerts(request):
    """
        Vue qui permet d'afficher l'historique des concerts pour chaque année

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    liste_des_evenements_tmp = Evenement.objects.order_by("-date")
    liste_des_evenements = OrderedDict()

    for evenement in liste_des_evenements_tmp:

        liste_des_evenements.setdefault(evenement.date.year, []).append(evenement)

    liste_des_annees = list(liste_des_evenements.keys())

    return render(request, "historique_des_concerts.html", {"liste_des_annees": liste_des_annees})


# ==================================================
def liste_des_evenements_de_l_annee(request, annee):
    """
        Vue qui permet d'afficher l'historique des concerts pour l'année spécifiée

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    annee_int = int(annee)

    liste_des_evenements_de_l_annee_tmp = Evenement.objects.order_by("-date")
    liste_des_evenements_de_l_annee = [ evenement for evenement in liste_des_evenements_de_l_annee_tmp if evenement.date.year == annee_int ]

    return render(request, "evenements_de_l_annee.html", {"annee": annee_int, "liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee})


# ===============================================
def voir_programme(request, id_evenement, annee):
    """
        Vue qui permet d'afficher le programme de l'évènement choisi

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param id_evenement: identifiant de l'évènement choisi
        :type id_evenement: str

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    evenement_choisi = Evenement.objects.filter(pk=id_evenement)

    if len(evenement_choisi) > 1:

        # à améliorer
        msg = "Erreur --- vue abonnement_evenement --- filtre nom : plus d'une personne"
        raise ValueError(msg)

    else:

        for obj in evenement_choisi:

            evenement_choisi = obj

    return render(request, "voir_programme.html", {"evenement_choisi": evenement_choisi, "annee": annee})


# ===================================
@login_required
@user_passes_test(personne_autorisee)
def photos(request):
    """
        Vue qui permet d'afficher les photos

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    liste_des_annees_tmp = Photo.objects.order_by("-date_de_l_evenement")
    liste_des_annees = OrderedDict()

    for photo in liste_des_annees_tmp:

        liste_des_annees.setdefault(photo.date_de_l_evenement.year, []).append(photo)

    return render(request, "photos.html", {"liste_des_annees": liste_des_annees})


# ==============================================
@login_required
@user_passes_test(personne_autorisee)
def ajouter_photos(request):
    """
        Vue du formulaire permettant l'ajout de photos

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Ajout de photos"
    classe_pour_envoi_formulaire = "js-ajouter-photos-creation-formulaire"
    titre_du_bouton_pour_validation = "Ajouter la(les) photo(s)"
    id_champ_date = "#id_date_de_l_evenement"
    formulaire = PhotoForm

    # Création du contexte
    donnees = {
        "url_pour_action": url_pour_action,
        "titre_du_formulaire": titre_du_formulaire,
        "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
        "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
        "id_champ_date": id_champ_date,
        "formulaire": formulaire
    }

    return creation_formulaire_outils_du_chef(request, donnees)


# ==============================================
@login_required
@user_passes_test(personne_autorisee)
def liste_des_photos_pour_annee(request, annee):
    """
        Vue qui permet d'afficher les photos pour une année donnée

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    annee_int = int(annee)

    liste_des_photos_de_l_annee = Photo.objects.order_by("-date_de_l_evenement")
    liste_des_evenements_de_l_annee = [ photo.nom_de_l_evenement for photo in liste_des_photos_de_l_annee if photo.date_de_l_evenement.year == annee_int ]
    liste_des_evenements_de_l_annee = set(liste_des_evenements_de_l_annee)

    return render(request, "photos_de_l_annee.html", {"liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee, "annee": annee})


# ===================================================
@login_required
@user_passes_test(personne_autorisee)
def voir_photos_evenement(request, evenement, annee):
    """
        Vue qui permet d'afficher les photos pour l'évènement sélectionné par le visiteur pour une année donnée

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param evenement: évènement sélectionné par le visiteur
        :type evenement: str

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    annee_int = int(annee)

    liste_des_photos_de_l_evenement_pour_l_annee_tmp = Photo.objects.order_by("date_de_l_evenement")
    liste_des_photos_de_l_evenement_pour_l_annee_tmp = [ photo for photo in liste_des_photos_de_l_evenement_pour_l_annee_tmp if photo.date_de_l_evenement.year == annee_int ]

    liste_des_photos_de_l_evenement_pour_l_annee = [ photo for photo in liste_des_photos_de_l_evenement_pour_l_annee_tmp if photo.nom_de_l_evenement == evenement ]

    return render(request, "photos_de_l_evenement_de_l_annee.html", {"liste_des_photos_de_l_evenement_pour_l_annee": liste_des_photos_de_l_evenement_pour_l_annee,
                                                                     "evenement":evenement,
                                                                     "annee":annee})


# ==============================================
@login_required
@user_passes_test(personne_autorisee)
def ajouter_videos(request):
    """
        Vue du formulaire permettant l'ajout de vidéos

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_evenement.__name__
    titre_du_formulaire = "Ajout de vidéos"
    classe_pour_envoi_formulaire = "js-ajouter-videos-creation-formulaire"
    titre_du_bouton_pour_validation = "Ajouter la(les) vidéo(s)"
    id_champ_date = "#id_date_de_l_evenement"
    formulaire = VideoForm

    # Création du contexte
    donnees = {
        "url_pour_action": url_pour_action,
        "titre_du_formulaire": titre_du_formulaire,
        "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
        "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
        "id_champ_date": id_champ_date,
        "formulaire": formulaire
    }

    return creation_formulaire_outils_du_chef(request, donnees)


# ===================================
@login_required
@user_passes_test(personne_autorisee)
def videos(request):
    """
        Vue qui permet d'afficher une vidéo

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    # return render(request, "lire_videos.html")
    liste_des_annees_tmp = Video.objects.order_by("-date_de_l_evenement")
    liste_des_annees = OrderedDict()

    for video in liste_des_annees_tmp:

        liste_des_annees.setdefault(video.date_de_l_evenement.year, []).append(video)

    return render(request, "videos.html", {"liste_des_annees": liste_des_annees})


# ==============================================
@login_required
@user_passes_test(personne_autorisee)
def liste_des_videos_pour_annee(request, annee):
    """
        Vue qui permet d'afficher les vidéos pour une année donnée

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    annee_int = int(annee)

    liste_des_videos_de_l_annee = Video.objects.order_by("-date_de_l_evenement")
    liste_des_evenements_de_l_annee = [ video.nom_de_l_evenement for video in liste_des_videos_de_l_annee if video.date_de_l_evenement.year == annee_int ]
    liste_des_evenements_de_l_annee = set(liste_des_evenements_de_l_annee)

    return render(request, "videos_de_l_annee.html", {"liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee, "annee": annee})


# ===================================
@login_required
@user_passes_test(personne_autorisee)
def voir_videos_evenement(request, evenement, annee):
    """
        Vue qui permet d'afficher les vidéos pour l'évènement sélectionné par le visiteur pour une année donnée

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param evenement: évènement sélectionné par le visiteur
        :type evenement: str

        :param annee: année choisie par le visiteur
        :type annee: str (converti automatiquement par django lors de l'utilisation d'expression régulières dans les URLs)

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    annee_int = int(annee)

    liste_des_videos_de_l_evenement_pour_l_annee_tmp = Video.objects.order_by("date_de_l_evenement")
    liste_des_videos_de_l_evenement_pour_l_annee_tmp = [ video for video in liste_des_videos_de_l_evenement_pour_l_annee_tmp if video.date_de_l_evenement.year == annee_int ]

    liste_des_videos_de_l_evenement_pour_l_annee = [ video for video in liste_des_videos_de_l_evenement_pour_l_annee_tmp if video.nom_de_l_evenement == evenement ]

    return render(request, "videos_de_l_evenement_de_l_annee.html", {"liste_des_videos_de_l_evenement_pour_l_annee": liste_des_videos_de_l_evenement_pour_l_annee,
                                                                     "evenement": evenement,
                                                                     "annee": annee})


# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
def les_outils_du_chef(request):
    """
        Vue qui permet d'afficher les outils du chef

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    liste_des_outils_tmp = []

    liste_des_outils_tmp.append(['creation_evenement', 'Créer un évènement', 'bouton_outils_du_chef js-creation-evenement'])
    liste_des_outils_tmp.append(['creation_article', 'Créer un article', 'bouton_outils_du_chef js-creation-article'])
    liste_des_outils_tmp.append(['creation_article_de_presse', 'Créer un article de presse', 'bouton_outils_du_chef js-creation-article-de-presse'])
    liste_des_outils_tmp.append(['creation_soutien', 'Créer un soutien', 'bouton_outils_du_chef js-creation-soutien'])
    liste_des_outils_tmp.append(['ajouter_photos', 'Ajouter des photos', 'bouton_outils_du_chef js-ajouter-photos'])
    liste_des_outils_tmp.append(['ajouter_videos', 'Ajouter des vidéos', 'bouton_outils_du_chef js-ajouter-videos'])

    liste_des_outils = [ {
                          "url": outil[0],
                          "nom": outil[1],
                          "classe": outil[2]
                         } for outil in liste_des_outils_tmp ]

    return render(request, "les_outils_du_chef.html", {"liste_des_outils": liste_des_outils})


# ==================================================================================================
# UTILISATION
# ==================================================================================================

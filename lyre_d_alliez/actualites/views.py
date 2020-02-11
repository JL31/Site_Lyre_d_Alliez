# coding: utf-8

"""
    Module de gestion des vues pour l'application "actualites"
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

from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.urls import reverse

from lyre_d_alliez.views import acces_restreint_au_chef, envoi_mail

from actualites.forms import EvenementForm, ArticleForm, CommentaireForm, AbonnementEvenementForm

from actualites.models import Evenement, Article, Commentaire, Abonnement

from locale import setlocale, LC_TIME
from datetime import datetime


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

# ==================================================================================================
# VUES
# ==================================================================================================

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

    return render(request, "actualites/agenda.html", {"liste_des_evenements": liste_des_evenements})


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
    data["html_form"] = render_to_string("actualites/formulaire_abonnement_evenement.html", context, request=request)

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
                message_d_erreur = "Problème lors de l'envoi d'une alerte mail à un abonné"

                donnees = { "sujet": sujet, "message": message, "message_d_erreur": message_d_erreur }

                envoi_mail(donnees)

    return HttpResponseRedirect(reverse("accueil"))


# ======================
def calendrier(request):
    """
        Vue qui permet de voir le calendrier

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "actualites/calendrier.html")


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

    return render(request, "actualites/liste_des_articles.html", {"liste_des_articles": liste_des_articles})


# ====================================================
def recuperation_commentaires(reference_de_l_article):
    """
        Fonction pour la récupération des commentaires de l'article

        :param reference_de_l_article: référence de l'article (sous forme d'id)
        :type reference_de_l_article: int

        :return: un dictionnaire contenant :
                 - la liste des commentaires de l'article [django.db.models.query.QuerySet]
                 - l'article [actualites.models.Article]
        :rtype: dict
    """

    # Récupération du contenu de l'article sélectionné
    # ------------------------------------------------

    article = Article.objects.filter(id=reference_de_l_article)

    # Récupération de la liste des commentaires de l'article sélectionné
    # ------------------------------------------------------------------

    donnees = dict()

    liste_des_commentaires = None
    article_obj = None

    if len(article) > 1:

        # à améliorer
        msg = "Erreur --- vue lire_article --- filtre id : plus d'un article"
        raise ValueError(msg)

    else:

        for obj in article:

            article_obj = obj
            liste_des_commentaires = Commentaire.objects.filter(articles=obj).order_by("-date")

    donnees = {"liste_des_commentaires": liste_des_commentaires,
               "article_obj": article_obj
              }

    return donnees


# =====================================================================
def requete_recuperation_commentaires(request, reference_de_l_article):
    """
        Requête pour la récupération des commentaires de l'article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param reference_de_l_article: référence de l'article (sous forme d'id)
        :type reference_de_l_article: int

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    donnees_commentaires = recuperation_commentaires(reference_de_l_article)

    context = {"liste_des_commentaires": donnees_commentaires["liste_des_commentaires"]}
    data["html_form"] = render_to_string("actualites/liste_des_commentaires.html", context, request=request)

    return JsonResponse(data)


# ===================================================================
def requete_soumission_commentaires(request, reference_de_l_article):
    """
        Requête pour la soumission d'un commentaire pour l'article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param reference_de_l_article: référence de l'article (sous forme d'id)
        :type reference_de_l_article: int

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    donnees_commentaires = recuperation_commentaires(reference_de_l_article)

    if request.method == "POST":

        form = CommentaireForm(request.POST)

        if form.is_valid():

            commentaire = form.save(commit=False)
            commentaire.date = timezone.now()
            commentaire.articles = donnees_commentaires["article_obj"]
            commentaire.redacteur = request.user.membre
            commentaire.save()

    return JsonResponse(data)


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

    # Récupération des commentaires associés à l'article sélectionné
    # --------------------------------------------------------------

    donnees_commentaires = recuperation_commentaires(reference_de_l_article)

    # Gestion du formulaire permettant l'ajout d'un commentaire à l'article sélectionné
    # ---------------------------------------------------------------------------------

    form_commentaires = CommentaireForm()

    contexte = {"article": donnees_commentaires["article_obj"],
                "liste_des_commentaires": donnees_commentaires["liste_des_commentaires"],
                "form": form_commentaires,
                "url_pour_action": requete_soumission_commentaires.__name__,
                "nom_classe_formulaire": "formulaire-ajout-commentaire",
                "titre_bouton_envoi": "Envoyer le commentaire",
                "nom_classe_bouton_envoi": "js-ajout-commentaire",
                "url_pour_data_url": requete_recuperation_commentaires.__name__,
                "template_affichage_commentaires": "actualites/liste_des_commentaires.html"
               }

    return render(request, "actualites/lecture_article.html", contexte)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
def creation_formulaire(request, donnees):
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

        if request.FILES:

            for fichier in request.FILES.getlist("fichier"):

                form = donnees["formulaire"](request.POST, request.FILES)

                if form.is_valid():

                    element = form.save(commit=False)
                    element.nom_du_fichier = fichier.name
                    element.fichier = fichier
                    element.save()

                    data["form_is_valid"] = True

                else:

                    data["form_is_valid"] = False

        else:

            form = donnees["formulaire"](request.POST, request.FILES)
            form.save()

            if form.is_valid():

                data["form_is_valid"] = True

            else:

                data["form_is_valid"] = False

    else:

        form = donnees["formulaire"]()

    context = {"form": form}
    context.update(donnees)
    del context["formulaire"]

    data["html_form"] = render_to_string("actualites/formulaire_actualites.html", context, request=request)

    return JsonResponse(data)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
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

    return creation_formulaire(request, donnees)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
def creation_article(request):
    """
        Vue du formulaire permettant la création d'un nouvel article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_article.__name__
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

    return creation_formulaire(request, donnees)


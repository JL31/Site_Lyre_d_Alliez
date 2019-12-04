from django.shortcuts import render

# Create your views here.
# coding: utf-8

"""
    Module de gestion des vues pour l'application "les outils du chef"
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

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required, user_passes_test

from lyre_d_alliez.views import acces_restreints_au_chef, personne_autorisee
from les_outils_du_chef.forms import EvenementForm, ArticleForm, ArticleDepresseForm, SoutienForm, PhotoForm, VideoForm


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

    return render(request, "les_outils_du_chef/les_outils_du_chef.html", {"liste_des_outils": liste_des_outils})


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

    data["html_form"] = render_to_string("les_outils_du_chef/formulaire_outils_du_chef.html", context, request=request)

    return JsonResponse(data)


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

    return creation_formulaire_outils_du_chef(request, donnees)


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

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_article_de_presse.__name__
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

    # Définition des valeurs des paramètres du contexte
    url_pour_action = creation_soutien.__name__
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


# ===================================
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
    url_pour_action = ajouter_photos.__name__
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


# ===================================
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
    url_pour_action = ajouter_videos.__name__
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


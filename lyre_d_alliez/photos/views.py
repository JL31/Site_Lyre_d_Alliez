# coding: utf-8

"""
    Module de gestion des vues pour l'application "photos"
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

from lyre_d_alliez.views import personne_autorisee, acces_restreints_au_chef

from photos.models import Photo

from photos.forms import PhotoForm

from collections import OrderedDict


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

    return render(request, "photos/photos.html", {"liste_des_annees": liste_des_annees})


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

    return render(request, "photos/photos_de_l_annee.html", {"liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee, "annee": annee})


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

    return render(request, "photos/photos_de_l_evenement_de_l_annee.html", {"liste_des_photos_de_l_evenement_pour_l_annee": liste_des_photos_de_l_evenement_pour_l_annee,
                                                                            "evenement": evenement,
                                                                            "annee": annee})


# =========================================
@login_required
@user_passes_test(acces_restreints_au_chef)
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

    data["html_form"] = render_to_string("photos/formulaire_photos.html", context, request=request)

    return JsonResponse(data)


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

    return creation_formulaire(request, donnees)


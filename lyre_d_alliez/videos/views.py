# coding: utf-8

"""
    Module de gestion des vues pour l'application "videos"
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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from lyre_d_alliez.views import personne_autorisee
from videos.models import Video

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
def videos(request):
    """
        Vue qui permet d'afficher une vidéo

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance
        :rtype: django.http.response.HttpResponse
    """

    liste_des_annees_tmp = Video.objects.order_by("-date_de_l_evenement")
    liste_des_annees = OrderedDict()

    for video in liste_des_annees_tmp:

        liste_des_annees.setdefault(video.date_de_l_evenement.year, []).append(video)

    return render(request, "videos/videos.html", {"liste_des_annees": liste_des_annees})


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

    return render(request, "videos/videos_de_l_annee.html", {"liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee, "annee": annee})


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

    return render(request, "videos/videos_de_l_evenement_de_l_annee.html", {"liste_des_videos_de_l_evenement_pour_l_annee": liste_des_videos_de_l_evenement_pour_l_annee,
                                                                            "evenement": evenement,
                                                                            "annee": annee})


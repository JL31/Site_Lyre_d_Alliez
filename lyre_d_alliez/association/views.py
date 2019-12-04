# coding: utf-8

"""
    Module de gestion des vues pour l'application "association"
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

from lyre_d_alliez.forms import LISTE_DES_INSTRUMENTS

from lyre_d_alliez.models import Membre
from actualites.models import Evenement
from association.models import ArticleDePresse, Soutien

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

    return render(request, "association/bureau.html", {"chef": chef, "liste_des_membres_du_bureau": liste_des_membres_du_bureau})


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

    return render(request, "association/les_pupitres.html", {"dico_instrument_membres": dico_instrument_membres})


# ==============================
def articles_de_presse(request):
    """
        Vue qui permet de lire un article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    liste_des_articles_de_presse = ArticleDePresse.objects.all()

    return render(request, "association/articles_de_presse.html", {"liste_des_articles_de_presse": liste_des_articles_de_presse})


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

    return render(request, "association/historique_des_concerts.html", {"liste_des_annees": liste_des_annees})


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

    return render(request, "association/evenements_de_l_annee.html", {"annee": annee_int, "liste_des_evenements_de_l_annee": liste_des_evenements_de_l_annee})


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

    return render(request, "association/voir_programme.html", {"evenement_choisi": evenement_choisi, "annee": annee})


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

    return render(request, "association/soutiens.html", {"liste_des_soutiens": liste_des_soutiens})


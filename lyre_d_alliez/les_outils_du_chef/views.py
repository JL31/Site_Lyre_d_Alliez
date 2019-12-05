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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from lyre_d_alliez.views import acces_restreints_au_chef


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


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

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from actualites.forms import CommentaireForm
from actualites.models import Evenement, Article, Commentaire


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

    return render(request, "actualites/lecture_article.html", {"article": article, "liste_des_commentaires": liste_des_commentaires, "form": form})


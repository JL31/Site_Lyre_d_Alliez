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
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.signals import post_save
from django.core.mail import mail_admins, send_mail
from django.contrib import messages

from .forms import MembreForm, LISTE_DES_INSTRUMENTS, EvenementForm, AbonnementEvenementForm, ArticleForm
from .models import Membre, Evenement, Abonnement, Article, Commentaire

from .secret_data import ADMINS, MOT_DE_PASSE

# from bootstrap_modal_forms.generic import BSModalCreateView

from collections import OrderedDict
from datetime import datetime
from locale import setlocale, LC_TIME
from smtplib import SMTPException


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================


# # ==============================================
# class VueAbonnementEvenement(BSModalCreateView):
#     """
#         ...
#     """
#
#     template_name = 'abonnement_evenement.html'
#     form_class = AbonnementEvenementForm
#     success_message = 'Abonnement réussi'
#     success_url = reverse_lazy('creation_evenement')


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

    return request.membre.est_membre or request.membre.est_membre_du_bureau or request.membre.est_le_chef

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

# =======================
def envoi_mail(**kwargs):
    """
        Fonction qui permet d'envoyer un mail
    """

    expediteur = ADMINS[0][1]
    destinataire = [ADMINS[0][1]]
    utilisateur = ADMINS[0][1]
    mot_de_passe = MOT_DE_PASSE

    try:

        send_mail(kwargs["sujet"], kwargs["message"], expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

    except SMTPException:

        msg = kwargs["msg_erreur"]
        raise SMTPException(msg)


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
    
@login_required
@user_passes_test(personne_autorisee)
# ===========================
def zone_de_partage(request):
    """
        Vue pour la zone de partage

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "sous_menu_zone_de_partage.html")

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
            return HttpResponseRedirect("/accueil/")

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

# ==============================
def creation_evenement(request):
    """
        Vue pour la création d'un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    if request.method == "POST":

        form = EvenementForm(request.POST)

        if form.is_valid():

            form.save()

            return HttpResponseRedirect("/accueil/")

    else:

        form = EvenementForm()

    return render(request, "EvenementForm.html", {"form": form})

# ====================================================
def abonnement_evenement(request, nom_de_l_evenement):
    """
        Vue pour la gestion d'un abonnement à un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param nom_de_l_evenement: nom de l'évènement auquel il faut rattacher l'abonnement
        :type nom_de_l_evenement: str

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    if request.method == "POST":

        form = AbonnementEvenementForm(request.POST)

        if form.is_valid():

            evenement = Evenement.objects.filter(nom=nom_de_l_evenement)

            if len(evenement) > 1:

                # à améliorer
                msg = "Erreur --- vue abonnement_evenement --- filtre nom : plus d'une personne"
                raise ValueError(msg)

            else:

                # mettre en place un système pour éviter les doublons
                # quid si un même visiteur souhaite programmer deux alertes à la même date ?

                adresse_mail_abonne = form.cleaned_data.get("adresse_email")
                date_de_l_alerte = form.cleaned_data.get("date_envoi_alerte")

                abonnement = Abonnement(adresse_mail_abonne=adresse_mail_abonne,
                                        date_de_l_alerte=date_de_l_alerte)
                abonnement.save()

                for obj in evenement:

                    obj.abonnements.add(abonnement)

                    setlocale(LC_TIME, "fr-FR")     # permet d'obtenir la date au format local (ici Fr)
                    msg = "Votre demande d'abonnement a bien été prise en compte. Vous recevrez un email pour vous alerter le {} à l'adresse suivante : {}".format(date_de_l_alerte.strftime("%A %d %B %Y"), adresse_mail_abonne)
                    messages.info(request, msg)

            return HttpResponseRedirect("/actualites/agenda/")

    else:

        form = AbonnementEvenementForm()

    return render(request, "abonnement_evenement_bis.html", {"form": form, "nom_de_l_evenement": nom_de_l_evenement})

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

    return HttpResponseRedirect("/accueil/")

# ==================
def bureau(request):
    """
        Vue du bureau

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
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

# ============================
def creation_article(request):
    """
        Vue du formulaire permettant la création d'un nouvel article

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    if request.method == "POST":

        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()
            msg = "L'article a été crée avec succès"
            messages.info(request, msg)
            return HttpResponseRedirect("/accueil/")

    else:

        form = ArticleForm()

    return render(request, "ArticleForm.html", {"form": form})

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

        :param reference_de_l_article:
        :type reference_de_l_article:

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    article = Article.objects.filter(id=reference_de_l_article)
    liste_des_commentaires = None

    if len(article) > 1:

        # à améliorer
        msg = "Erreur --- vue lire_article --- filtre id : plus d'un article"
        raise ValueError(msg)

    else:

        for obj in article:

            article = obj

            liste_com = Commentaire.objects.all()
            print()
            print(liste_com)
            for it in liste_com:

                print()
                print(it.texte)
                print(it.article_set.all())

            print()
            liste_des_commentaires = Commentaire.objects.filter(article=obj)
            print(liste_des_commentaires)

    return render(request, "lecture_article.html", {"article": article, "liste_des_commentaires": liste_des_commentaires})


# ==================================================================================================
# SIGNAUX
# ==================================================================================================

# Envoi d'un mail aux admins en cas de création d'un nouveau compte Membre
post_save.connect(envoi_mail_admin_nouveau_membre, sender=Membre)


# ==================================================================================================
# UTILISATION
# ==================================================================================================

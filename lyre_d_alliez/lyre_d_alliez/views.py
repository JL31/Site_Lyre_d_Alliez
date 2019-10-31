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
from django.core.mail import mail_admins
from .forms import MembreForm, LISTE_DES_INSTRUMENTS, EvenementForm, AbonnementEvenementForm
from .models import Membre, Evenements, Abonnement

# from bootstrap_modal_forms.generic import BSModalCreateView
# from django.urls import reverse_lazy

from collections import OrderedDict

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
               "Merci de vérifier les informations renseignées et de lui attribuer soit : \n\n"
               "- l'accès à la zone membre ;\n"
               "- l'accès aux outils du chef.")

    mail_admins(sujet, message)


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

    liste_des_evenements = Evenements.objects.all()

    return render(request, "agenda.html", {"liste_des_evenements": liste_des_evenements})

# ==============================
def creation_evenement(request):
    """
        Vue pour la création d'un évènement

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
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
# def abonnement_evenement(request):
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

            evenement = Evenements.objects.filter(nom=nom_de_l_evenement)

            if len(evenement) > 1:

                # à améliorer
                raise ValueError

            else:

                abonnement = Abonnement(adresse_mail_abonne=form.cleaned_data.get("adresse_email"),
                                        date_de_l_alerte=form.cleaned_data.get("date_envoi_alerte"))
                abonnement.save()

                for obj in evenement:

                    obj.abonnements.add(abonnement)

            return HttpResponseRedirect("/actualites/agenda/")

    else:

        form = AbonnementEvenementForm()

    return render(request, "abonnement_evenement_bis.html", {"form": form, "nom_de_l_evenement": nom_de_l_evenement})


# ==================================================================================================
# SIGNAUX
# ==================================================================================================

# Envoi d'un mail aux admins en cas de création d'un nouveau compte Membre
post_save.connect(envoi_mail_admin_nouveau_membre, sender=Membre)


# ==================================================================================================
# UTILISATION
# ==================================================================================================

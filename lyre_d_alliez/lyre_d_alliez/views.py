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
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

from lyre_d_alliez.forms import MembreForm
from lyre_d_alliez.models import Membre
from association.models import Soutien

from lyre_d_alliez.secret_data import ADMINS
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


# =======================================================================
@receiver(post_save, sender=Membre)
def envoi_mail_admin_nouveau_membre(sender, instance, created, **kwargs):
    """
        Fonction qui permet d'envoyer un mail à l'admin pour l'informer qu'un nouveau membre a été créé

        :param sender: le modèle qui émet le signal (la classe de modèle)
        :type sender: django.db.models.base.ModelBase

        :param instance: l'instance en cours d'enregistrement
        :type instance: lyre_d_alliez.models.Membre

        :param created: booléen qui permet de savoir si un nouvel enrgistrement est créé
        :type created: bool
    """

    if created:

        sujet = " Inscription d'un nouveau membre"
        message = ("{} vient de remplir le formulaire d'inscription à la zone des membres.\n\n"
                   "Merci de vérifier les informations renseignées et de lui attribuer les accès en tant que : \n\n"
                   "- membre ;\n"
                   "- membre du bureau ;\n"
                   "- chef.".format(instance.username))

        expediteur = ADMINS["default"]["login"]
        destinataire = (ADMINS["default"]["login"],)

        try:

            send_mail(sujet, message, expediteur, destinataire, fail_silently=False)

        except SMTPException as e:

            msg = ("Problème lors de l'envoi de mail après la création d'un compte membre"
                   "\n{}".format(e))
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

    instance.fichier.delete(False)


# ===============================
def envoi_mail(dico_des_donnees):
    """
        Fonction qui permet d'envoyer un mail

        :param dico_des_donnees: liste des paramètres nommés (sujet, message)
        ::type dico_des_donnees: dict
    """

    expediteur = ADMINS["default"]["login"]
    destinataire = (ADMINS["default"]["login"],)

    try:

        send_mail(dico_des_donnees["sujet"], dico_des_donnees["message"], expediteur, destinataire, fail_silently=False)

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

# ==================================================================================================
# CLASSES
# ==================================================================================================

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


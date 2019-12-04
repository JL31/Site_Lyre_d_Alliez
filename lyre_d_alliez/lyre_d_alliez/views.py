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
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.core.mail import mail_admins, send_mail
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout

from lyre_d_alliez.forms import MembreForm, AbonnementEvenementForm, DemandeDevenirSoutienForm, AuthentificationForm
from lyre_d_alliez.models import Membre
from actualites.models import Evenement, Abonnement
from association.models import Soutien

from lyre_d_alliez.secret_data import ADMINS, MOT_DE_PASSE

from datetime import datetime
from locale import setlocale, LC_TIME
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


# =================================
@receiver(post_save, sender=Membre)
def envoi_mail(sender, **kwargs):
    """
        Fonction qui permet d'envoyer un mail

        :param sender: l'instance du modèle Soutien qui est en cours de suppression
        :type sender: lyre_d_alliez.models.Soutien
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

    try:

        send_mail(sujet, message, expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

    except SMTPException:

        msg = "Problème lors de l'envoi de mail après la création d'un compte membre"
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


# ===================================
def envoi_mail_bis(dico_des_donnees):
    """
        Fonction qui permet d'envoyer un mail

        :param dico_des_donnees: liste des paramètres nommés (sujet, message)
        ::type dico_des_donnees: dict
    """

    expediteur = ADMINS[0][1]
    destinataire = [ADMINS[0][1]]
    utilisateur = ADMINS[0][1]
    mot_de_passe = MOT_DE_PASSE

    try:

        send_mail(dico_des_donnees["sujet"], dico_des_donnees["message"], expediteur, destinataire, fail_silently=False, auth_user=utilisateur, auth_password=mot_de_passe)

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
    data["html_form"] = render_to_string("formulaire_abonnement_evenement.html", context, request=request)

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
                msg_erreur = "Problème lors de l'envoi d'une alerte mail à un abonné"

                envoi_mail(sujet=sujet, message=message, msg_erreur=msg_erreur)

    return HttpResponseRedirect(reverse("accueil"))


# ========================================
def demande_pour_devenir_soutien(request):
    """
        Vue du formulaire permettant la demande pour devenir un soutien de l'asso

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = demande_pour_devenir_soutien.__name__
    titre_du_formulaire = "Demande pour devenir soutien de la Lyre d'Alliez"
    classe_pour_envoi_formulaire = "js-demande-pour-devenir-soutien-creation-formulaire"
    titre_du_bouton_pour_validation = "Envoyer la demande"
    id_champ_date = ""
    formulaire = DemandeDevenirSoutienForm

    # Création du contexte
    donnees = {
               "url_pour_action": url_pour_action,
               "titre_du_formulaire": titre_du_formulaire,
               "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
               "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
               "id_champ_date": id_champ_date,
               "formulaire": formulaire
              }

    return creation_formulaire_demande_pour_devenir_soutien(request, donnees)


# =====================================================================
def creation_formulaire_demande_pour_devenir_soutien(request, donnees):
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

        form = donnees["formulaire"](request.POST)

        if form.is_valid():

            # récupération des données du formulaire
            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            societe = form.cleaned_data["societe"]
            adresse_email = form.cleaned_data["adresse_email"]
            numero_de_telephone = form.cleaned_data["numero_de_telephone"]
            message = form.cleaned_data["message"]

            # définition du sujet du mail
            sujet = "Demande pour devenir soutien de l'asso"

            # définition des coordonnées de la personne qui envoie la demande de soutien
            # améliorable avec la version 3.6 et le formatted string literal
            coordonnees = ""

            if adresse_email != "" and numero_de_telephone == "":

                coordonnees = "adresse email : {}".format(adresse_email)

            elif adresse_email == "" and numero_de_telephone != "":

                coordonnees = "numéro de téléphone : {}".format(numero_de_telephone)

            elif adresse_email != "" and numero_de_telephone != "":

                coordonnees = "adresse email : {}\nnuméro de téléphone : {}".format(adresse_email, numero_de_telephone)

            # définition du début du message (selon si un nom de société a été renseigné ou non)
            if societe != "":

                debut_message = ("La société {} souhaite devenir soutien de l'association.\n"
                                 "La personne a contacter est {} {},").format(societe, prenom, nom)

            else:

                debut_message = "{} {} souhaite devenir soutien de l'association,".format(prenom, nom)

            # définition du message à envoyer
            message_a_envoyer = ("{} ses coordonnées sont :\n\n"
                                 "{}\n\n"
                                 "Voici son message :\n\n"
                                 "{}").format(debut_message, coordonnees, message)

            message_d_erreur = "Problème lors de l'envoi d'un mail de demande pour devenir soutien de l'asso"

            # envoi d'un mail contenant les données définies précédemment
            dico_des_donnees = {
                                "sujet": sujet,
                                "message": message_a_envoyer,
                                "message_d_erreur": message_d_erreur
                               }

            envoi_mail_bis(dico_des_donnees)

            data["form_is_valid"] = True

            msg = "La demande a été envoyée"
            messages.info(request, msg)

        else:

            data["form_is_valid"] = False

    else:

        form = donnees["formulaire"]()

    context = {"form": form}
    context.update(donnees)
    del context["formulaire"]

    data["html_form"] = render_to_string("formulaire_demande_devenir_soutien.html", context, request=request)

    return JsonResponse(data)


# ============================
def authentification(request):
    """
        Vue pour l'authentification

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = authentification.__name__
    titre_du_formulaire = "Authentification"
    classe_pour_envoi_formulaire = "js-authentification-creation-formulaire"
    titre_du_bouton_pour_validation = "Se connecter"
    id_champ_date = ""
    formulaire = AuthentificationForm

    # Création du contexte
    donnees = {
               "url_pour_action": url_pour_action,
               "titre_du_formulaire": titre_du_formulaire,
               "classe_pour_envoi_formulaire": classe_pour_envoi_formulaire,
               "titre_du_bouton_pour_validation": titre_du_bouton_pour_validation,
               "id_champ_date": id_champ_date,
               "formulaire": formulaire
    }

    return creation_formulaire_authentification(request, donnees)


# =========================================================
def creation_formulaire_authentification(request, donnees):
    """
        Vue qui permet d'afficher le formulaire pour l'authentification

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param donnees: données issues de la vue appelant la vue
        :type donnees: dict

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    if request.method == "POST":

        form = donnees["formulaire"](request.POST)

        if form.is_valid():

            login_utilisateur = form.cleaned_data["login"]
            mot_de_passe_utilisateur = form.cleaned_data["mot_de_passe"]

            utilisateur = authenticate(username=login_utilisateur, password=mot_de_passe_utilisateur )

            if utilisateur is not None:

                data["user_authenticated"] = True
                login(request, utilisateur)
                data["url_pour_redirection"] = reverse("accueil")

                msg = "Bienvenue"
                messages.info(request, msg)

            else:

                data["user_authenticated"] = False

            data["form_is_valid"] = True

        else:

            data["form_is_valid"] = False

    else:

        form = donnees["formulaire"]()

    context = {"form": form}
    context.update(donnees)
    del context["formulaire"]

    data["html_form"] = render_to_string("formulaire_authentification.html", context, request=request)

    return JsonResponse(data)


# ==============================
def verification_login(request):
    """
        Vue qui permet de vérifier que le login existe bien

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    login = request.GET.get("login", None)
    data = {"login_existe": Membre.objects.filter(username__iexact=login).exists()}

    return JsonResponse(data)


# =======================
def deconnexion(request):
    """
        Vue qui permet de déconnecter un utilisateur

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    context = dict()
    context["url_pour_action"] = deconnexion.__name__

    data = dict()
    data["url_pour_redirection"] = reverse("accueil")
    data["html_content"] = render_to_string("deconnexion.html", context, request=request)

    if request.method == "POST":

        logout(request)

    return JsonResponse(data)


# ==================================================================================================
# UTILISATION
# ==================================================================================================

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

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from lyre_d_alliez.views import acces_restreint_au_chef, envoi_mail

from lyre_d_alliez.forms import LISTE_DES_INSTRUMENTS
from association.forms import ArticleDepresseForm, SoutienForm, DemandeDevenirSoutienForm

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


# =============================================
def affichage_programme(request, id_evenement):
    """
        Vue qui permet d'afficher le programme de l'évènement choisi

        :param request: instance de HttpRequest ou de HttpResponseRedirect
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param id_evenement: identifiant de l'évènement choisi
        :type id_evenement: str

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    # Définition des valeurs des paramètres du contexte
    url_pour_action = affichage_programme.__name__

    nom_de_l_evenement = Evenement.objects.get(id=id_evenement)
    titre = "Programme du {}".format(nom_de_l_evenement)

    programme = Evenement.objects.get(id=id_evenement).programme

    # Création du contexte
    donnees = {
               "url_pour_action": url_pour_action,
               "titre": titre,
               "programme": programme,
               "id_evenement ": id_evenement,
              }

    return recuperation_contenu_du_programme(request, donnees)


# ======================================================
def recuperation_contenu_du_programme(request, donnees):
    """
        Vue qui permet de récupérer le contenu du programme à afficher dans la fenêtre Bootstrap

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param donnees: données issues de la vue appelant cette vue
        :type donnees: dict

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    data = dict()

    context = {}
    context.update(donnees)

    data["html_form"] = render_to_string("association/formulaire_affichage_programme_evenement.html", context, request=request)

    return JsonResponse(data)


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

            envoi_mail(dico_des_donnees)

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

    data["html_form"] = render_to_string("association/formulaire_demande_devenir_soutien.html", context, request=request)

    return JsonResponse(data)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
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

    data["html_form"] = render_to_string("association/formulaire_association.html", context, request=request)

    return JsonResponse(data)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
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

    return creation_formulaire(request, donnees)


# =========================================
@login_required
@user_passes_test(acces_restreint_au_chef)
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

    return creation_formulaire(request, donnees)


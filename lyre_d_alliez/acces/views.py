# coding: utf-8

"""
    Module de gestion des vues pour l'application "acces"
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

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from lyre_d_alliez.views import personne_autorisee

from lyre_d_alliez.models import Membre

from acces.forms import AuthentificationForm


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

    data["html_form"] = render_to_string("acces/formulaire_authentification.html", context, request=request)

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
    data["html_content"] = render_to_string("acces/deconnexion.html", context, request=request)

    if request.method == "POST":

        logout(request)

    return JsonResponse(data)


# ==========================
def acces_interdit(request):
    """
        Vue pour l'accès interdit à une page du site

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    return render(request, "acces/acces_interdit.html")


# ======================================
@login_required
@user_passes_test(personne_autorisee)
def changement_du_mot_de_passe(request):
    """
        Vue permettant la modification du mot de passe d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    url_pour_redirection = 'accueil'
    option_modification = 'deconnexion'

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a bien été mis-à-jour')

            return redirect(url_pour_redirection)

    else:

        form = PasswordChangeForm(request.user)

    return render(request, 'acces/modification_donnees_membre.html', {'form': form,
                                                                      'url_pour_redirection': url_pour_redirection,
                                                                      'option_modification': option_modification
                                                                     })


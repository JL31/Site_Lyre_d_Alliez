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

from random import choice

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from acces.forms import AuthentificationForm
from acces.token import default_token_generator
from lyre_d_alliez.forms import UpdateMembreForm, MembreForm
from lyre_d_alliez.models import Membre
from lyre_d_alliez.secret_data import ADMIN_USERNAME
from lyre_d_alliez.views import personne_autorisee, envoi_mail, acces_restreint_aux_admins
from .forms import ConfirmPasswordForm, EnvoiLienCreationProfilMembreForm


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================


# =======================
def generate_random_id():
    """
        Fonction qui permet la géénration aléatoire d'un identifiant.
        L'identifiant est constitué de 20 caractères pris dans les caractères affichables (depuis string.printable)

        :return: l'identifiant
        :rtype: str
    """

    nombre_de_caracteres = 20
    liste_des_carcateres = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-.:;<=>?@^_`{|}~[]'

    return "".join([ choice(liste_des_carcateres) for _ in range(nombre_de_caracteres) ])


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

decorators = [login_required, user_passes_test(personne_autorisee)]

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

    if login == ADMIN_USERNAME:

        data = {"login_existe": True}

    else:

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

    return render(request, 'acces/gestion_des_donnees_membre.html', {'form': form,
                                                                      'url_pour_redirection': url_pour_redirection,
                                                                      'option_modification': option_modification
                                                                     })


# ====================================
@method_decorator(decorators, name='dispatch')
class ConfirmPasswordView(UpdateView):
    """
        Vue basée sur une classe permettant de demander la confirmation pour la suppression du profil d'un membre
    """

    # configuration de la classe
    form_class = ConfirmPasswordForm
    template_name = 'acces/gestion_des_donnees_membre.html'
    success_url = reverse_lazy('supprimer_le_compte')

    # variables à ajouter dans le contexte du template
    url_pour_redirection = 'accueil'
    option_modification = 'confirmation_suppression_compte'

    # ===================
    def get_object(self):
        """
            Méthode qui récupère l'objet

            ... ... ... finir de compléter ... ... ...
        """

        return self.request.user

    # ===================================
    def get_context_data(self, **kwargs):
        """
            Méthode qui permet de surcharger le contexte

            ... ... ... finir de compléter ... ... ...
        """

        context = super(ConfirmPasswordView, self).get_context_data(**kwargs)
        context['url_pour_redirection'] = self.url_pour_redirection
        context['option_modification'] = self.option_modification

        return context


# ===================================
@login_required
@user_passes_test(personne_autorisee)
def supprimer_le_compte(request):
    """
        Vue permettant la suppression du profil d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    url_pour_redirection = 'accueil'

    try:

        membre = Membre.objects.get(pk=request.user.pk)
        membre.delete()
        messages.success(request, "Votre profil a bien été supprimé")

    except Membre.DoesNotExist:

        messages.error(request, "Ce membre n'existe pas")
        return redirect(url_pour_redirection)

    except Exception as e:

        messages.error(request, "Une erreur inattendue s'est produite : {}".format(e.message))
        return redirect(url_pour_redirection)

    return redirect(url_pour_redirection)


# ===================================
@login_required
@user_passes_test(personne_autorisee)
def donnees_personnelles(request):
    """
        Vue permettant la visualisation des données personnelles d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse
        :rtype: django.http.response.HttpResponse
    """

    url_pour_redirection = 'accueil'
    option_modification = 'consultation'

    return render(request, 'acces/gestion_des_donnees_membre.html', {'url_pour_redirection': url_pour_redirection,
                                                                      'option_modification': option_modification})


# =====================================================
@login_required
@user_passes_test(personne_autorisee)
def modification_des_donnees_personnelles(request, id):
    """
        Vue permettant la modification des données personnelles d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param id: clé primaire permettant d'identifier le membre
        :type id: integer

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    membre = get_object_or_404(Membre, id=id)

    nom_du_template = "acces/modification_des_donnees_personnelles.html"

    if request.method == "POST":

        form = UpdateMembreForm(request.POST, instance=membre)

    else:

        form = UpdateMembreForm(instance=membre)

        instruments_choisis = tuple([ instrument.replace("'", "") for instrument in membre.get_instruments_as_list() ])
        form.initial["instruments"] = instruments_choisis

    return enregistrer_les_modifications(request, form, nom_du_template)


# ================================================================
@login_required
@user_passes_test(personne_autorisee)
def enregistrer_les_modifications(request, form, nom_du_template):
    """
        Vue qui permet d'enregistrer les modifications dans les données personnelles du membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :param form: formulaire qui gère les données personnelles des membres
        :type form: lyre_d_alliez.forms.UpdateMembreForm

        :param nom_du_template: le nom du template qui va contenir le formulaire de modification des données personnelles
        :type nom_du_template: string

        :return: instance de JsonResponse
        :rtype: django.http.response.JsonResponse
    """

    donnees = {}

    if request.method == "POST":

        if form.is_valid():

            form.save()
            donnees["formulaire_valide"] = True

        else:

            donnees["formulaire_valide"] = False

    contexte = {"form": form}
    donnees["html_form"] = render_to_string(nom_du_template, contexte, request=request)

    return JsonResponse(donnees)


# ===================================================
def creation_profil_membre(request, *args, **kwargs):
    """
        Vue pour la création du profil d'un membre

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    assert "random_id_1" in kwargs and "random_id_2" in kwargs and "jeton" in kwargs

    random_id_1 = kwargs["random_id_1"]
    random_id_2 = kwargs["random_id_2"]
    jeton = kwargs["jeton"]

    if default_token_generator.check_token(random_id_1, random_id_2, jeton):

        if request.method == "POST":

            form = MembreForm(request.POST, request.FILES)

            if form.is_valid():

                form.save()
                msg = "Le profil a été crée avec succès, merci d'attendre l'email d'activation de votre compte"
                messages.info(request, msg)

                return HttpResponseRedirect(reverse("accueil"))

        else:

            form = MembreForm()
            return render(request, "acces/MembreForm.html", {"form": form,
                                                             "random_id_1": random_id_1,
                                                             "random_id_2": random_id_2,
                                                             "jeton": jeton})

    else:

        return render(request, "acces/ErreurAccesFormulaireCreationProfilMembre.html")


# =============================================================
@login_required
@user_passes_test(acces_restreint_aux_admins)
def formulaire_pour_envoi_mail_creation_profil_membre(request):
    """
        Vue pour l'affichage du formulaire qui va permettre d'envoyer un mail à un futur membre
        afin qu'il puisse compléter son profil en vue de sa création

        :param request: instance de HttpRequest
        :type request: django.core.handlers.wsgi.WSGIRequest

        :return: instance de HttpResponse ou de HttpResponseRedirect
        :rtype: django.http.response.HttpResponse | django.http.response.HttpResponseRedirect
    """

    if request.method == "POST":

        form = EnvoiLienCreationProfilMembreForm(request.POST)

        if form.is_valid():

            random_id_1 = generate_random_id()
            random_id_2 = generate_random_id()
            jeton = default_token_generator.make_token(random_id_1, random_id_2)

            sujet = "[ Site de la Lyre d'Alliez ]"

            # en_tete_lien = "http://{}".format(Site.objects.get_current().domain)
            en_tete_lien = "localhost:8000"
            lien = reverse("creation_profil_membre", args=(random_id_1, random_id_2, jeton))
            lien_complet = "{}{}".format(en_tete_lien, lien)

            message_fr = ("Hello,\n\n"
                          "Si tu veux créer un compte sur le site de la Lyre merci de cliquer sur le lien suivant :\n\n"
                          "{}\n\n"
                          "Attention, ce lien n'est utilisable qu'une seule fois et il sera actif pendant xxx.\n\n"
                          "Passé ce délai il faudra nous demander de t'en générer un nouveau ;-)\n\n"
                          "A bientôt et bonne inscription ^^\n\n"
                          "L'équipe d'administration du site de la Lyre d'Alliez").format(lien_complet)

            message_en = ("Hello,\n\n"
                          "If you want to subscribe to the Lyre website please click on the link bellow :\n\n"
                          "{}\n\n"
                          "Be aware that this link will only be available once and it will be active for xxx .\n\n"
                          "After that period you will have to ask us to generate you a new one ;-)\n\n"
                          "See you soon and good subscription ^^\n\n"
                          "The Lyre d'Alliez website administration team").format(lien_complet)

            message = ("{}\n\n"
                       "___________________________________________________________________________________________\n\n"
                       "{}\n\n").format(message_fr, message_en)

            dico_des_donnees = {"sujet": sujet,
                                "message": message,
                                }

            envoi_mail(dico_des_donnees)

            msg = "Un email contenant un lien à usage unique a été envoyé au futur membre"
            messages.info(request, msg)

            return HttpResponseRedirect(reverse("accueil"))

    else:

        form = EnvoiLienCreationProfilMembreForm()

    return render(request, "acces/EnvoiMailCreationProfilMembreForm.html", {"form": form})


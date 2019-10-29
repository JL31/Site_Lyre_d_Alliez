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
from .forms import MembreForm
from .models import Membre


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

# ==================================================================================================
# FUNCTIONS
# ==================================================================================================


# ===================================
def test_personne_autorisee(request):
    """
        Fonction de test pour vérifier si le visiteur est autorisée à accéder à certaines pages

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

    # sujet = " Isncription d'un nouveau membre"
    # message = ("Une personne vient de remplir le formulaire d'inscription à la zone des membres.\n\n"
    #            "Merci de vérifier les informations renseignées et de lui attribuer soit : \n\n"
    #            "- l'accès à la zone membre ;\n"
    #            "- l'accès aux outils du chef.")
    #
    # mail_admins(sujet, message)
    pass


# ==================================================================================================
# VUES
# ==================================================================================================


# ========================
def test_accueil(request):
    """
        Vue de test de la page d'accueil
    """
    
    return render(request, "base_etendue.html")
    

# ===========================
def test_actualites(request):
    """
        Vue de test pour les actualités
    """
    
    return render(request, "sous_menu_actualites.html")
    

# ===========================
def test_association(request):
    """
        Vue de test pour l'association
    """
    
    return render(request, "sous_menu_association.html")
    

@login_required
@user_passes_test(test_personne_autorisee)
# ================================
def test_zone_de_partage(request):
    """
        Vue de test pour la zone de partage
    """

    return render(request, "sous_menu_zone_de_partage.html")


# =======================================
def test_creation_profil_membre(request):
    """
        Vue de test pour la création du profil d'un membre
    """

    if request.method == "POST":

        form = MembreForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return HttpResponseRedirect("/accueil/")

    else:

        form = MembreForm()

    return render(request, "test_MembreForm.html", {"form": form})
    

# ===============================
def test_acces_interdit(request):
    """
        Vue de test pour l'accès interdit à une page du site
    """
    
    return render(request, "acces_interdit.html")
    

# ==================================================================================================
# UTILISATION
# ==================================================================================================

# Signaux

# envoi d'un mail aux admins en cas de création d'un nouveau compte Membre
post_save.connect(envoi_mail_admin_nouveau_membre, sender=Membre)

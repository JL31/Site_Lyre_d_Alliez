# coding: utf-8

"""
    acces URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/2.1/topics/http/urls/

    Examples:

    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')

    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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

from django.urls import path, re_path
from acces.views import *


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

# ==================================================================================================
# CLASSES
# ==================================================================================================

# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

urlpatterns = [
    path('authentification/', authentification, name='authentification'),
    path('verification_login/', verification_login, name="verification_login"),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('acces_interdit/', acces_interdit, name='acces_interdit'),
    path('changement_du_mot_de_passe/', changement_du_mot_de_passe, name='changement_du_mot_de_passe'),
    path('confirmation_suppression_compte/', ConfirmPasswordView.as_view(), name='confirmation_suppression_compte'),
    path('supprimer_le_compte/', supprimer_le_compte, name='supprimer_le_compte'),
    path('donnees_personnelles/', donnees_personnelles, name='donnees_personnelles'),
    re_path('^modification_des_donnees_personnelles/(?P<id>\d+)/$', modification_des_donnees_personnelles, name='modification_des_donnees_personnelles'),

    # Gestion de la création d'un profil membre
    path('formulaire_pour_envoi_mail_creation_profil_membre/', formulaire_pour_envoi_mail_creation_profil_membre, name='formulaire_pour_envoi_mail_creation_profil_membre'),
    path('creation_profil_membre/<random_id_1>/<random_id_2>/<jeton>/', creation_profil_membre, name='creation_profil_membre'),
]

# coding: utf-8

"""
    association URL Configuration

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
from django.contrib.flatpages.views import flatpage
from association.views import *


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
    path('presentation/', flatpage, {'url': '/association/presentation/'}, name='presentation'),
    path('bureau/', bureau, name='bureau'),
    path('les_pupitres/', les_pupitres, name='les_pupitres'),
    path('articles_de_presse/', articles_de_presse, name='articles_de_presse'),
    path('historique_des_concerts/', historique_des_concerts, name='historique_des_concerts'),
    re_path('liste_des_evenements_de_l_annee/(?P<annee>\d{4})/$', liste_des_evenements_de_l_annee, name='liste_des_evenements_de_l_annee'),
    re_path('voir_programme/(?P<id_evenement>\d*)/(?P<annee>\d{4})/$', voir_programme, name='voir_programme'),
    path('soutiens/', soutiens, name='soutiens'),
]

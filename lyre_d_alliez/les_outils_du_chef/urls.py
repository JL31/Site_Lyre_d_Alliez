# coding: utf-8

"""
    les outils du chef URL Configuration

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

from django.urls import path

from les_outils_du_chef.views import *
from actualites.views import creation_evenement, creation_article
from association.views import creation_article_de_presse, creation_soutien
from photos.views import ajouter_photos
from videos.views import ajouter_videos


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
    path('', les_outils_du_chef, name='les_outils_du_chef'),
    path('creation_evenement/', creation_evenement, name='creation_evenement'),
    path('creation_article/', creation_article, name='creation_article'),
    path('creation_article_de_presse/', creation_article_de_presse, name='creation_article_de_presse'),
    path('creation_soutien/', creation_soutien, name='creation_soutien'),
    path('ajouter_photos/', ajouter_photos, name='ajouter_photos'),
    path('ajouter_videos/', ajouter_videos, name='ajouter_videos'),
]

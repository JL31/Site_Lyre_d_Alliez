# coding: utf-8

"""
    lyre_d_alliez URL Configuration

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
__date__ = '10/2019'
__status__ = 'dev'


# ==================================================================================================
# IMPORTS
# ==================================================================================================

from django.contrib import admin
from django.urls import path, include
from .views import *

# Pour la gestion des images (en dév)
from django.conf.urls.static import static
from django.conf import settings


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
    path('admin/', admin.site.urls),

    path('accueil/', accueil, name='accueil'),

    # Menu et sous-menus : Actualités
    path('actualites/', include('actualites.urls')),

    # Menu et sous-menus  : Association
    path('association/', include('association.urls')),

    # Menu Photos
    path('photos/', include('photos.urls')),

    # Menu Vidéos
    path('videos/', include('videos.urls')),

    # Menu et sous-menus  : Zone de partage
    # path('zone_de_partage/', zone_de_partage, name='zone_de_partage'),

    # Menu Les outils du chef
    path('les_outils_du_chef/', include('les_outils_du_chef.urls')),

    # Autres
    path('creation_profil_membre/', creation_profil_membre, name='creation_profil_membre'),

    # Connexion / déconnexion
    path('acces/', include('acces.urls')),
]

# Pour la gestion des images (en dév)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from django.urls import path
from django.contrib.flatpages.views import flatpage
from django.contrib.auth.views import LoginView, LogoutView
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
    path('accueil/', test_accueil, name='accueil'),
    path('actualites/', test_actualites, name='actualites'),
    path('association/', test_association, name='association'),
    path('association/presentation', flatpage, {'url': '/association/presentation/'}, name='presentation'),
    path('association/bureau', flatpage, {'url': '/association/bureau/'}, name='bureau'),
    path('zone_de_partage/', test_zone_de_partage, name='zone_de_partage'),
    path('creation_profil_membre/', test_creation_profil_membre, name='creation_profil_membre'),
    path('connexion/', LoginView.as_view(template_name='connexion.html'), name='connexion'),
    path('deconnexion/', LogoutView.as_view(template_name='deconnexion.html'), name='deconnexion'),
    path('acces_interdit/', test_acces_interdit, name='acces_interdit'),
]

# Pour la gestion des images (en dév)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

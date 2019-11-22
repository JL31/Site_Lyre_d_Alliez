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
from django.urls import path, re_path
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

    path('accueil/', accueil, name='accueil'),

    # Menu et sous-menus : Actualités
    path('actualites/', actualites, name='actualites'),
    path('actualites/agenda/', agenda, name='agenda'),
    path('actualites/articles/', liste_des_articles, name='liste_des_articles'),
    re_path(r'^actualites/article/(?P<reference_de_l_article>\d+)/$', lire_article, name='lire_article'),

    # Menu et sous-menus  : Association
    path('association/', association, name='association'),
    path('association/presentation/', flatpage, {'url': '/association/presentation/'}, name='presentation'),
    path('association/bureau/', bureau, name='bureau'),
    path('association/les_pupitres/', les_pupitres, name='les_pupitres'),
    path('association/articles_de_presse/', articles_de_presse, name='articles_de_presse'),
    path('association/historique_des_concerts/', historique_des_concerts, name='historique_des_concerts'),
    re_path('association/liste_des_evenements_de_l_annee/(?P<annee>\d{4})/$', liste_des_evenements_de_l_annee, name='liste_des_evenements_de_l_annee'),
    re_path('association/voir_programme/(?P<id_evenement>\d*)/(?P<annee>\d{4})/$', voir_programme, name='voir_programme'),
    path('association/soutiens/', soutiens, name='soutiens'),

    # Menu Photos
    path('photos/', photos, name='photos'),
    re_path('photos/liste_des_photos_pour_annee/(?P<annee>\d{4})/$', liste_des_photos_pour_annee, name='liste_des_photos_pour_annee'),
    re_path('photos/voir_photos_evenement/(?P<evenement>.*)/(?P<annee>\d{4})/$', voir_photos_evenement, name='voir_photos_evenement'),

    # Menu Vidéos
    path('videos/', videos, name='videos'),
    re_path('videos/liste_des_videos_pour_annee/(?P<annee>\d{4})/$', liste_des_videos_pour_annee, name='liste_des_videos_pour_annee'),
    re_path('videos/voir_videos_evenement/(?P<evenement>.*)/(?P<annee>\d{4})/$', voir_videos_evenement, name='voir_videos_evenement'),

    # Menu et sous-menus  : Zone de partage
    # path('zone_de_partage/', zone_de_partage, name='zone_de_partage'),

    # Menu Les outils du chef
    path('les_outils_du_chef/', les_outils_du_chef, name='les_outils_du_chef'),

    path('creation_evenement/', creation_evenement, name='creation_evenement'),
    path('creation_article/', creation_article, name='creation_article'),
    path('creation_article_de_presse/', creation_article_de_presse, name='creation_article_de_presse'),
    path('creation_soutien/', creation_soutien, name='creation_soutien'),
    path('ajouter_photos/', ajouter_photos, name='ajouter_photos'),
    path('ajouter_videos/', ajouter_videos, name='ajouter_videos'),

    # Autres
    path('creation_profil_membre/', creation_profil_membre, name='creation_profil_membre'),
    re_path(r'^abonnement_evenement/(?P<id_evenement>\d+)/$', abonnement_evenement, name='abonnement_evenement'),
    path('envoi_alerte_abonne/', envoi_alerte_abonne, name='envoi_alerte_abonne'),

    path('demande_pour_devenir_soutien/', demande_pour_devenir_soutien, name='demande_pour_devenir_soutien'),

    # Connexion / deconnexion
    path('connexion/', LoginView.as_view(template_name='connexion.html'), name='connexion'),
    path('deconnexion/', LogoutView.as_view(template_name='deconnexion.html'), name='deconnexion'),
    path('acces_interdit/', acces_interdit, name='acces_interdit'),
]

# Pour la gestion des images (en dév)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

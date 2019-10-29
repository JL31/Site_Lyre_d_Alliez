# coding: utf-8

"""
    Module de gestion des modèles
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

from django.db import models
from django.contrib.auth.models import User


# ==================================================================================================
# INITIALISATIONS
# ==================================================================================================

LISTE_DES_INSTRUMENTS = (('clarinette si b', 'clarinette si b'),
                         ('clarinette basse', 'clarinette basse'),
                         ('flute traversiere', 'flute traversière'),
                         ('flute traversiere basse', 'flute traversière basse'),
                         ('piccolo', 'piccolo'),
                         ('xylophone_marimba', 'xylophone / marimba'),
                         ('piano', 'piano'),
                         ('saxophone soprano', 'saxophone soprano'),
                         ('saxophone alto', 'saxophone alto'),
                         ('saxophone tenor', 'saxophone ténor'),
                         ('saxophone baryton', 'saxophone baryton'),
                         ('saxophone basse', 'saxophone basse'),
                         ('trombone', 'trombone'),
                         ('trombone basse', 'trombone basse'),
                         ('euphonium', 'euphonium'),
                         ('tuba', 'tuba'),
                         ('guitare seche', 'guitare sèche'),
                         ('guitare electrique', 'guitare électrique'),
                         ('guitare acoustique', 'guitare acoustique'),
                         ('mandoline', 'mandoline'),
                         ('guitare basse', 'guitare basse'),
                         ('trompette', 'trompette'),
                         ('batterie', 'batterie')
                        )


# ==================================================================================================
# CLASSES
# ==================================================================================================

# =================
class Membre(User):
    """
        Classe qui décrit le modèle des membres
    """
    
    # liaison avec le modèle User
    user = models.OneToOneField(User, parent_link=True, unique=True, on_delete=models.CASCADE)
    
    # avatar = models.ImageField(null=False, blank=False, upload_to="avatars/")
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    
    # description = models.TextField(null=True, blank=False, max_length=500)
    description = models.TextField(null=True, blank=True, max_length=500)
    
    instrument = models.CharField(null=False, blank=False, max_length=255, choices=LISTE_DES_INSTRUMENTS, default='clarinette si b')
    
    chant = models.BooleanField(null=False, blank=True, default=False)
    est_membre = models.BooleanField(null=False, blank=True, default=False)
    est_membre_du_bureau = models.BooleanField(null=False, blank=True, default=False)
    est_le_chef = models.BooleanField(null=False, blank=True, default=False)

    class Meta:
        """
            Configuration/définition des options de metadonnées du modèle
        """
        
        verbose_name = "membre"
        ordering = ["avatar", 
                    "username",
                    "first_name",
                    "email",
                    "description",
                    "instrument",
                    "chant",
                    "est_membre",
                    "est_membre_du_bureau",
                    "est_le_chef"
                   ]

    def __str__(self):
        """
            Permet de faciliter la reconnaissance des objets lors de l'administration
        """
        
        return self.username


# ==================================================================================================
# FUNCTIONS
# ==================================================================================================

# ==================================================================================================
# UTILISATION
# ==================================================================================================

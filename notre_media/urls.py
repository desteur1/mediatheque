
from django.urls import path
from . import views

urlpatterns = [
# gestion des membres
path('membre/',views.liste_membre, name='liste_membre'),
path('membre/ajouter/',views.ajouter_membre, name='ajouter_membre'),
path('membre/<int:id>/modifier/',views.modifier_membre, name='modifier_membre'),

# gestion des livre/medias
path('livres/',views.liste_medias, name='liste_medias'),
path('livres/ajouter/',views.ajouter_media, name='ajouter_media'),
path('livres/<int:id>modifier/',views.modifier_media, name='modifier_media'),
]



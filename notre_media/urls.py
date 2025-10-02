
from notre_livre.urls import urlpatterns

urlpatterns = [
# gestion des membres
path('membre/',views.liste_membre, name='liste_membre'),
path('membre/ajouter/',views.ajouter_membre, name='ajouter_membre'),
path('membre/<int:id>/modifier/',views.modifier_membre, name='modifier_membre'),

# gestion des livre/medias
path('livres/',views.liste_livres, name='liste_livres'),
path('livres/ajouter/',views.ajouter_livres, name='ajouter_livres'),
path('livres/<int:id>modifier',views.modifier_livres, name='modifier_livres'),
]



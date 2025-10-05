
from django.urls import path
from . import views

urlpatterns =[
    path ('', views.liste_medias, name='liste_medias'),
    path ('<int:id>/', views.detail_medias, name='detail_medias'),
    path('<int:media_id>/emprunter/', views.emprunter_media, name='emprunter_media'),
    path('<int:emprunt_id>/retourner/', views.retourner_media, name='retourner_media'),
]
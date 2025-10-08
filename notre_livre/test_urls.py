import pytest
from django.urls import reverse, resolve  # reverse = URL builder, resolve = view matcher
from notre_livre import views  # import views to match against resolved URLs
from .models import Media, Membre, Emprunt
from datetime import timedelta, date

pytestmark = pytest.mark.django_db  # enable DB access for view tests

#  Test that '' resolves to liste_medias view
def test_liste_medias_url_resolves():
    url = reverse('public:liste_medias')  # builds '/'
    assert resolve(url).func == views.liste_medias  # confirms it maps to the correct view

#  Test that '<int:id>/' resolves to detail_medias view
def test_detail_medias_url_resolves():
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre')
    url = reverse('public:detail_medias', args=[media.id])  # builds '/<id>/'
    assert resolve(url).func == views.detail_medias

#  Test that '<int:media_id>/emprunter/' resolves to emprunter_media view
def test_emprunter_media_url_resolves():
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre')
    url = reverse('public:emprunter_media', args=[media.id])  # builds '/<media_id>/emprunter/'
    assert resolve(url).func == views.emprunter_media

#  Test that '<int:emprunt_id>/retourner/' resolves to retourner_media view
def test_retourner_media_url_resolves():
    membre = Membre.objects.create(nom='Desteur', email='desteur@example.com', mot_de_passe='x')
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre')
    emprunt = Emprunt.objects.create(membre=membre, media=media, rendu=False, date_retour=date.today() + timedelta(days=7))
    url = reverse('public:retourner_media', args=[emprunt.id])  # builds '/<emprunt_id>/retourner/'
    assert resolve(url).func == views.retourner_media
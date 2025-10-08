import pytest
from django.urls import reverse # used to resolve view names to URLs
from .models import Media, Membre, Emprunt
from datetime import timedelta, date

# Apply the django_db marker to all tests in this file so they can access the database
pytestmark = pytest.mark.django_db # enables DB access for all tests

# Test the media listing view
def test_liste_medias_view(client):
    # Create one media item to ensure the view has something to display
    Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre')
    # Simulate(mimic) a GET request to the 'liste_medias' view
    response = client.get(reverse('public:liste_medias'))
    # Check that the response was successful (HTTP 200)
    assert response.status_code == 200
    # Ensure the context contains the 'medias' variable
    assert 'medias' in response.context
    # Confirm that exactly one media item is present
    assert response.context['medias'].count() == 1


def test_detail_medias_view(client):
    # Create a media item to test its detail page
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre')
    response = client.get(reverse('public:detail_medias', args=[media.id]))
    assert response.status_code == 200
    assert 'media' in response.context
    assert response.context['media'].titre == '1984'


def test_emprunter_media_view(client):
    # Create a media item that is available for borrowing
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre', disponible= True)
    # Simulate a POST request to borrow the media with name and email
    response = client.post(reverse('public:emprunter_media', args=[media.id]), data={
        'nom': 'Desteur',
        'email': 'desteur@example.com'
    }, follow=True) # follow redirects to get final response
    # Check that the response was successful
    assert response.status_code == 200
    # Refresh the media object from the database to get updated state
    media.refresh_from_db()
    # Confirm that the media is now marked as unavailable
    assert media.disponible is False #  should be marked unavailable


def test_retourner_media_view(client):
    # Create a member who will borrow the media
    membre = Membre.objects.create(nom='Desteur', email='desteur@example.com', mot_de_passe='x')
    # Create a media item that is currently unavailable (borrowed)
    media = Media.objects.create(titre='1984', auteur='George Orwell', type_media='livre', disponible=False)
    # Create an active loan for that media
    emprunt = Emprunt.objects.create(
        membre=membre, media=media,
        rendu=False, # not yet returned
        date_retour=date.today() + timedelta(days=7)) # due in the future

    # Simulate a GET request to return the media
    response = client.get(reverse('public:retourner_media',args=[emprunt.id]), follow=True)
    # Check that the response was successful
    assert response.status_code == 200
    # Refresh both objects from the database to get updated state
    emprunt.refresh_from_db()
    media.refresh_from_db()
    # Confirm that the loan is now marked as returned
    assert emprunt.rendu is True
    assert media.disponible is True
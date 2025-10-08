import pytest
from .models import Membre,Media, Emprunt
from datetime import timedelta, date

# Create your tests here.
pytestmark = pytest.mark.django_db   #  Enables DB access for all tests below



def test_membre_password_check():
    membre = Membre(nom='Desteur', email='desteur@example.com')
    membre.set_password('secret123')
    assert membre.check_password('secret123') is True
    assert membre.check_password('wrongpass') is False


def test_membre_str():
    membre = Membre(nom='Desteur')
    assert str(membre) == 'Desteur'



def test_media_str():
    media = Media(titre='Le Petit Prince')
    assert str(media) == 'Le Petit Prince'


def test_emprunt_sets_date_retour():
    membre = Membre.objects.create(nom='Test', email='test@example.com', mot_de_passe='x')
    media = Media.objects.create(titre='Livre', auteur='Auteur', type_media='livre')
    emprunt = Emprunt.objects.create(membre=membre, media=media)
    assert emprunt.date_retour == emprunt.date_emprunt + timedelta(days=7)




def test_emprunt_retard():
    membre = Membre.objects.create(nom="Test", email="test@example.com", mot_de_passe="x")
    media = Media.objects.create(titre="Livre", auteur="Auteur", type_media="livre")
    emprunt = Emprunt.objects.create(
        membre=membre,
        media=media,
        # date_retour set to yesterday, date.today() gives today's date, timedelta(days=1) =subtracts one day
        date_retour=date.today() - timedelta(days=1), # saying this item was due yesterday for the test
        rendu=False
    )
    assert emprunt.est_en_retard() is True


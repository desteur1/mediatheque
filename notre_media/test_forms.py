import pytest
from .forms import MembreForm
from notre_livre.models import Membre

pytestmark = pytest.mark.django_db  #  enable DB access for form.save()


#  Test valid form input and password hashing
def test_membre_form_valid_and_password_hash():
    form_data = {
        'nom' : 'Desteur',
        'email': 'desteur@example.com',
        'mot_de_passe': 'secret123',
        'est_bibliothecaire': False
    }
    form = MembreForm(data=form_data)
    assert form.is_valid()  #  form should pass validation

    membre = form.save()
    assert isinstance(membre, Membre) #  should return a Membre instance
    assert membre.check_password('secret123') is True #  password should be hashed and verifiable


#  Test missing required fields
def test_membre_form_missing_field():
    form_data = {
        'nom': '',
        'email': '',
        'mot_de_passe': '',
        'est_bibliothecaire': False
    }
    form = MembreForm(data=form_data)
    assert not form.is_valid()  #  should fail validation

    assert  'nom' in form.errors
    assert 'email' in form.errors
    assert 'mot_de_passe' in form.errors

#  Test that raw password is not stored directly
def test_membre_form_does_not_store_plain_password():
    form_data = {
        'nom': 'Desteur',
        'email': 'desteur@example.com',
        'mot_de_passe': 'plainpassword',
        'est_bibliothecaire': True
    }
    form = MembreForm(data=form_data)
    membre = form.save()
    assert membre.mot_de_passe != 'plainpassword'  #  should be hashed
    assert  membre.check_password('plainpassword') is True #  still matches
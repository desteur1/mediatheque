import pytest
from .forms_livre  import MediaForm

def test_media_form_valis():
    form_data= {
        'titre': 'Le Petie Prince',
        'auteur': 'Antoine de saint-Exupéry',
        'type_media': 'livre',
        'disponible': True
    }
    form = MediaForm(data=form_data)
    assert form.is_valid()

def test_media_form_missing_required_fileds():
    form_data = {
        'titre': '', # missing title

        'auteur': '',
        'type_media': '',
    }
    form = MediaForm(data=form_data)
    assert not form.is_valid()  #  form should fail validation
    assert 'titre' in form.errors # error should mention missing title
    assert 'auteur' in form.errors
    assert 'type_media' in form.errors


def test_media_form_default_disponible():
    form_data = {
        'titre': '1984',  # valid title
        'auteur': 'George Orwell',
        'type_media': 'livre'
        # 'disponible' omitted
    }
    form =MediaForm(data=form_data)
    assert form.is_valid()   #  form should still be valid
    media = form.save(commit=False)  # create model instance without saving
    assert media.disponible is True # should default to True from model

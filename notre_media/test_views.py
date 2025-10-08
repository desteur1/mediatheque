import pytest
from django.urls import reverse
from notre_livre.models import Membre

pytestmark = pytest.mark.django_db  # enable DB access for all tests

#  Test  successful login for a bibliothecaire
def test_login_view_success(client):
    # Create a bibliothecaire
    membre = Membre.objects.create(
        nom='Desteur',
        email='desteur@example.com',
        est_bibliothecaire=True
    )
    membre.set_password('secret123')  # Hash the password
    membre.save()

    # Simulate login POST request
    response = client.post(reverse('gestion:login'), data={
        'email': 'desteur@example.com',
        'mot_de_passe': 'secret123'
    }, follow=True)

    # Check that login was successful and session is set
    assert response.status_code == 200
    assert client.session['membre_id'] == membre.id

#  Test login fails for non-bibliothécaire
def test_login_view_rejects_non_bibliothecaire(client):
    # Create a regular member (not a bibmiothecaire)
    membre = Membre.objects.create(
        nom='NotLib',
        email='notlib@example.com',
        est_bibliothecaire=False
    )
    membre.set_password('secret123')
    membre.save()

    # Attempt login
    response = client.post(reverse('gestion:login'), data={
        'email': 'notlib@example.com',
        'mot_de_passe': 'secret123'
    })
    # Check that the correct error message is shown
    assert 'accès réservé aux bibliothécaires' in response.context['form'].non_field_errors()

# Test login fails with wrong password
def test_login_view_wrong_password(client):
    # Create a valid bibliothecaire
    membre = Membre.objects.create(
        nom='Desteur',
        email='desteur@example.com',
        est_bibliothecaire=True
    )
    membre.set_password('secret123')
    membre.save()

    # Attempt login with wrong password
    response = client.post(reverse('gestion:login'), data={
        'email': 'desteur@example.com',
        'mot_de_passe': 'wrongpass'
    })

    # Check that the correct error message is shown
    assert 'Mot de passe incorrect' in response.context['form'].non_field_errors()

#  Test logout clears session
def test_logout_view(client):
    # Create and log in a bibliothecaire
    membre = Membre.objects.create(
        nom='Desteur',
        email='desteur@example.com',
        est_bibliothecaire=True
    )
    membre.set_password('secret123')
    membre.save()

    # Log in
    client.post(reverse('gestion:login'), data={
        'email': 'desteur@example.com',
        'mot_de_passe': 'secret123'
    })
    # Confirm session is set
    assert 'membre_id' in client.session

    # Log out
    response = client.get(reverse('gestion:logout'), follow=True)
    # Confirm session is cleared
    assert response.status_code == 200
    assert 'membre_id' not in client.session

# Test Protected view redirects to se connecter if not authenticated
def test_ajouter_media_requires_bibliothecaire(client):
    # Try accessing a protected view without logging in
    response = client.get(reverse('gestion:ajouter_media'), follow=True)
    # Confirm redirect happened
    assert response.redirect_chain  # should redirect to se connecter
    assert response.status_code == 200
    # Confirm login page is shown
    assert 'se connecter' in response.content.decode().lower()







    #In Django, client is a test client — a simulated browser that lets you send requests to your views just like a real user would
    #we're using Pytest with pytest-django, which automatically provides client as a fixture. That means:
    #we don’t need to create it manually.
    # Pytest injects it into your test function when you declare it as a parameter.

    # .non_field_errors() returns a list of validation errors not tied to a specific field.
    # These are added using form.add_error(None, "message") in the view logic.
    # Useful for catching general errors like "Mot_de_passe incorrect" or "Accès réservé aux bibliothécaires".
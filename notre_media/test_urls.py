import pytest
from django.urls import reverse
from notre_livre.models import Membre

pytestmark = pytest.mark.django_db

# Helper: create a logged-in bibliothécaire
def login_bibliothecaire(client):
    membre = Membre.objects.create(
        nom='Desteur',
        email='desteur@example.com',
        est_bibliothecaire=True
    )
    membre.set_password('secret123')
    membre.save()
    client.post(reverse('gestion:login'), data={
        'email': 'desteur@example.com',
        'mot_de_passe': 'secret123'
    })
    return membre

# ✅ Test all public and protected URLs
def test_all_gestion_urls(client):
    # Public URLs
    public_urls = [
        reverse('gestion:login'),
        reverse('gestion:logout'),
        reverse('gestion:liste_membres'),
        reverse('gestion:liste_medias'),
    ]

    for url in public_urls:
        response = client.get(url)
        assert response.status_code in [200, 302]

    # Protected URLs (require login)
    protected_urls = [
        reverse('gestion:ajouter_membre'),
        reverse('gestion:modifier_membre', args=[1]),
        reverse('gestion:ajouter_media'),
        reverse('gestion:modifier_media', args=[1]),
    ]

    # Without login: should redirect
    for url in protected_urls:
        response = client.get(url)
        assert response.status_code in [302]

    # With login: should succeed
    login_bibliothecaire(client)

    for url in protected_urls:
        response = client.get(url)
        assert response.status_code in [200, 404]  # 404 if ID doesn't exist
from django.db import models

# Create your models here.


class Membre(models.Model):
    nom = models.CharField(max_length=150)
    email = models.CharField(unique=True)

    def __str__(self):
        return self.nom

class Media(models.Model):
    TYPE_CHOICES = [
    ('livre', 'Livre'),
    ('cd', 'CD'),
    ('dvd', 'DVD'),
    ('jeu', 'Jeu de plateau'),
    ]
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150)
    type_media = models.CharField(max_length=10,choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True,blank=True)

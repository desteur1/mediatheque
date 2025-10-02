from django import forms
from .models import Membre, Media, Emprunt

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'email']



class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur', 'type_media', 'disponible']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media', 'date_retour']
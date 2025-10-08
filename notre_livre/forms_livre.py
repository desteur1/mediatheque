from django import forms
from .models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur', 'type_media'] # ommited 'disponible' for the default to be true when ommited to check the checkbox

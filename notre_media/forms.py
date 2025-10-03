from django import forms
from notre_livre.models import Membre, Media, Emprunt

class MembreForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Membre
        fields = ['nom', 'email', 'mot_de_passe', 'est_bibliothecaire']

    def save(self, commit = True):
        membre = super().save(commit=False)
        membre.set_password(self.cleaned_data["mot_de_passe"])
        if commit:
            membre.save()
        return membre

class LoginForm(forms.Form):
    email =forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)



class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur', 'type_media', 'disponible']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media', 'date_retour', 'rendu']
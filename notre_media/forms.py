from django import forms
from notre_livre.models import Membre, Media, Emprunt

class MembreForm(forms.ModelForm):
    #- widget=forms.PasswordInput → replaces the default text box with a password-style input.
    mot_de_passe = forms.CharField(widget=forms.PasswordInput) #  hides password input in the form

    class Meta:
        model = Membre  #  links the form to the Membre model
        fields = ['nom', 'email', 'mot_de_passe', 'est_bibliothecaire'] #  fields shown in the form

    def save(self, commit = True):
        membre = super().save(commit=False)  #  creates a Membre instance but doesn't save yet
        membre.set_password(self.cleaned_data["mot_de_passe"])  #  hashes the password securely
        if commit:
            membre.save()  #  saves the instance to the database
        return membre  #  returns the saved or unsaved instance

class LoginForm(forms.Form):
    email =forms.EmailField() #  validates email format
    mot_de_passe = forms.CharField(widget=forms.PasswordInput) #  hides password input



class MediaForm(forms.ModelForm):
    class Meta:
        model = Media  #  links to the Media model
        fields = ['titre', 'auteur', 'type_media', 'disponible']  #  fields shown in the form


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt #  links to the Emprunt model
        fields = ['membre', 'media', 'date_retour', 'rendu']
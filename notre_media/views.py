from venv import create

from django.shortcuts import render, redirect, get_object_or_404
from notre_livre.models import Membre, Media
from django.contrib import messages

from .forms import MembreForm, MediaForm, LoginForm



# ------decorateur pour restreindre l'accès aux biblithécaires ------
def bibliothecaire_required(view_func):
    def wrapper(request, *args, **kwargs):
        membre_id = request.session.get('membre_id') # récupère l'id du membre connecté
        if not membre_id:
            return redirect('gestion:login') # redirection login bibliothécaire
        try:
            membre = Membre.objects.get(id=membre_id)
        except Membre.DoesNotExist:
            return redirect('gestion:login')
        if not membre.est_bibliothecaire: # si ce n'est pas un bibliothecaire
            return redirect('gestion:login')
        return view_func(request,*args,**kwargs) # autorisé - exécuter la vue(view)
    return wrapper

# ============ Membre ==================
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliotheque/membres/liste.html', {'membres': membres})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                membre = Membre.objects.get(email=email)
                if not membre.est_bibliothecaire:
                    form.add_error(None, 'accès réservé aux bibliothécaires')
                elif membre.check_password(mot_de_passe):
                    request.session['membre_id'] = membre.id
                    return redirect('gestion:liste_medias')
                else:
                    form.add_error(None, 'Mot de passe incorrect')
            except Membre.DoesNotExist:
                form.add_error(None, 'Email non trouvé')
    else:
            form = LoginForm()


    return render(request, 'bibliotheque/membres/login.html', {'form': form})

def logout_view(request):
        request.session.flush()
        return redirect('gestion:login')



@bibliothecaire_required
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save() # sauvegarde le média
            return redirect('gestion:liste_membres') # utilise juste le name de l'URL
    else: # Get
         form = MembreForm() # formulaire vide pour GET

            # if POST invalid or GET
    return render(request, 'bibliotheque/membres/form_membre.html', {'form':form})
@bibliothecaire_required
def modifier_membre(request,id):
    membre = get_object_or_404(Membre,id=id)
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_membres') # utilise juste le name de l'URL
    else: # Get
        form = MembreForm(instance=membre)

            # if POST invalid or GET
    return render(request, 'bibliotheque/membres/form_membre.html', {'form':form})

# ================ Medias ================
def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliotheque/medias/liste.html', {'medias':medias})

@bibliothecaire_required
def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_medias') # utilise juste le name de l'URL
    else: # Get
         form = MediaForm()

    # if POST invalid or GET
    return render(request, 'bibliotheque/medias/form_media.html', {'form':form})
@bibliothecaire_required
def modifier_media(request,id):
    media = get_object_or_404(Media, id=id)
    if request.method == 'POST':
        form = MediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('gestion:liste_medias') # utilise juste le name de l'URL
    else: # Get
        form = MediaForm(instance=media)

        # if POST invalid or GET
    return render(request, 'bibliotheque/medias/form_media.html', {'form':form})






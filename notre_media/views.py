from django.shortcuts import render, redirect, get_object_or_404
from .models import Membre, Media
from .forms import MembreForm, MediaForm

# ============ Membre ==================
def liste_membre(request):
    membres = Membre.objects.all()
    return render(request, 'bibliotheque/membres/liste.html', {'membre': membres})

def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membre') # utilise juste le name de l'URL
        else: # Get
            form = MembreForm()

            # if POST invalid or GET
    return render(request, 'bibliotheque/membres/add.html', {'form':form})

def modifier_membre(request,id):
    membre = get_object_or_404(Membre,id=id)
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('liste_membre') # utilise juste le name de l'URL
        else: # Get
            form = MembreForm()

            # if POST invalid or GET
        return render(request, 'bibliotheque/membres/edit.html', {'form':form})

# ================ Medias ================
def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliotheque/medias/liste.html', {'medias':medias})


def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias') # utilise juste le name de l'URL
        else: # Get
            form = MediaForm()

    # if POST invalid or GET
    return render(request, 'bibliotheque/medias/add.html', {'form':form})

def modifier_media(request,id):
    media = get_object_or_404(Media, id=id)
    if request.method == 'POST':
        form = MediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('liste_medias') # utilise juste le name de l'URL
        else: # Get
            form = MediaForm()

        # if POST invalid or GET
    return render(request, 'bibliotheque/medias/edit.html', {'form':form})


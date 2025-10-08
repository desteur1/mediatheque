from django.shortcuts import render, redirect, get_object_or_404
from notre_livre.models import Membre, Media
from .forms import MembreForm, MediaForm, LoginForm



# ------decorateur pour restreindre l'accès aux biblithécaires ------
def bibliothecaire_required(view_func):
    def wrapper(request, *args, **kwargs):
        membre_id = request.session.get('membre_id') # récupère l'id du membre connecté
        if not membre_id:
            return redirect('gestion:login') # redirection login bibliothécaire
        try:
            membre = Membre.objects.get(id=membre_id)  #  fetch user from DB
        except Membre.DoesNotExist:
            return redirect('gestion:login') #  redirect if user not found
        if not membre.est_bibliothecaire: # si ce n'est pas un bibliothecaire
            return redirect('gestion:login')
        return view_func(request,*args,**kwargs) # autorisé - exécuter la vue(view)
    return wrapper

# ============ Membre ==================
def liste_membres(request):
    membres = Membre.objects.all()  #  get all members
    return render(request, 'bibliotheque/membres/liste.html', {'membres': membres})  #  render list


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  #  bind form with POST data
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                membre = Membre.objects.get(email=email)  #  find user by email
                if not membre.est_bibliothecaire:
                    form.add_error(None, 'accès réservé aux bibliothécaires')  #  not a bibliothecaire
                elif membre.check_password(mot_de_passe):
                    request.session['membre_id'] = membre.id #  save login session
                    return redirect('gestion:liste_medias')  #  redirect to media list
                else:
                    form.add_error(None, 'Mot de passe incorrect')  #  wrong password
            except Membre.DoesNotExist:
                form.add_error(None, 'Email non trouvé') #  email not found
    else:
            form = LoginForm()  #  empty form for GET


    return render(request, 'bibliotheque/membres/login.html', {'form': form}) #  render login form

def logout_view(request):
        request.session.flush() #  clear session
        return redirect('gestion:login')  #  redirect to se connecter



@bibliothecaire_required
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)  #  bind form with POST data
        if form.is_valid():
            form.save() # save new membre
            return redirect('gestion:liste_membres') # redirect to membre list
    else: # Get
         form = MembreForm() # formulaire vide pour GET

            # if POST invalid or GET
    return render(request, 'bibliotheque/membres/form_membre.html', {'form':form})  #  render form

@bibliothecaire_required
def modifier_membre(request,id):
    membre = get_object_or_404(Membre,id=id)  #  fetch member or 404
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)  #  bind form with existing member
        if form.is_valid():
            form.save() #  save changes
            return redirect('gestion:liste_membres')  #  redirect to member list
    else: # Get
        form = MembreForm(instance=membre)  #  pre-filled form for GET

            # if POST invalid or GET
    return render(request, 'bibliotheque/membres/form_membre.html', {'form':form})  #  render form

# ================ Medias ================
def liste_medias(request):
    medias = Media.objects.all()  #  get all media items
    return render(request, 'bibliotheque/medias/liste.html', {'medias':medias})  #  render list

@bibliothecaire_required
def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)  #  bind form with POST data
        if form.is_valid():
            form.save()  #  save new media
            return redirect('gestion:liste_medias') #  redirect to media list
    else: # Get
         form = MediaForm() #  empty form for GET

    # if POST invalid or GET
    return render(request, 'bibliotheque/medias/form_media.html', {'form':form}) #  render form
@bibliothecaire_required
def modifier_media(request,id):  #  fetch media or 404
    media = get_object_or_404(Media, id=id)
    if request.method == 'POST':
        form = MediaForm(request.POST, instance=media)  #  bind form with existing media
        if form.is_valid():
            form.save()  #  save changes
            return redirect('gestion:liste_medias') #  redirect to media list
    else: # Get
        form = MediaForm(instance=media)  #  pre-filled form for GET

        # if POST invalid or GET
    return render(request, 'bibliotheque/medias/form_media.html', {'form':form})  #  render form






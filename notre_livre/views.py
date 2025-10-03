from django.shortcuts import render, redirect, get_object_or_404
from .models import Media, Emprunt
from django.contrib import messages


def liste_medias(request):
    medias = Media.objects.all()  # récupère tous les médias
    return render(request, 'medias/display.html', {'medias':medias})

def detail_medias(request, id):
    media = get_object_or_404(Media, id=id) # récupère un média spécifique ou 404 si non trouvé
    return render(request, 'medias/detail.html', {'media': media}) # envoie la liste à display.html


def emprunter_media(request, media_id):
    media = get_object_or_404(Media, pk=media_id) # récupère le média choisi
    # Vérifier si c’est un jeu de plateau
    if media.type_media == "jeu":
        messages.error(request, "Les jeux de plateau ne peuvent pas être empruntés.")
        return redirect("public:liste_medias")

    # récupérer nom/email depuis un formulaire post
    if request.method == 'POST': # si le formulaire est soumis
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        if not nom or not email:
            messages.error(request, 'Veuillez fournir un nom et un email')
            return redirect("public:liste_medias")

        # Créer ou récupérer le membre
        membre, created =Membre.objects.get_or_create(email=email, defaults={'nom':nom})

        # Vérifie que le membre n'a pas déjà 3 emprunts ou d'emprunt en retard
        emprunts_actifs = Emprunt.objects.filter(membre=membre, rendu=False)
        if emprunts_actifs.count() >= 3:
            messages.error(request, 'Vous avez déjà 3 emprunts en cours.')
            return redirect('public:liste_medias')
        if any(e.est_en_retard() for e in emprunts_actifs):
            messages.error(request, f'Vous avez un emprunt en retard.')
            return redirect('public:liste_medias')


        # créer l'emprunt
        Emprunt.objects.create(membre=membre, media=media)
        messages.success(request, 'Vous avez emprunté {media.titre}. Retour prévu dans 7 jours.')
        return redirect('public:liste_medias')

    # Get : afficher un mini-formulaire nom/email pour emprunteur
    return render(request, 'medias/form_emprunt.html', {'media':media})

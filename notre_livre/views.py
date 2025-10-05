from django.shortcuts import render, redirect, get_object_or_404
from .models import Media, Emprunt, Membre
from django.contrib import messages
from datetime import date


def liste_medias(request):
    medias = Media.objects.all()  # récupère tous les médias
    membre = None
    emprunts = None

    membre_id = request.session.get('membre_id')
    if membre_id:
        membre = get_object_or_404(Membre, pk=membre_id)
        emprunts = Emprunt.objects.filter(membre=membre).order_by('-date_emprunt')
    return render(request, 'medias/display.html', {'medias':medias, 'membre':membre, 'emprunts':emprunts})

def detail_medias(request, id):
    media = get_object_or_404(Media, id=id) # récupère un média spécifique ou 404 si non trouvé
    return render(request, 'medias/detail.html', {'media': media}) # envoie la liste à display.html


def emprunter_media(request, media_id):
    media = get_object_or_404(Media, pk=media_id) # récupère le média choisi
    membre = None
    membre_id = request.session.get('membre_id')
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
        membre, created = Membre.objects.get_or_create(email=email, defaults={'nom':nom})
        request.session['membre_id'] = membre.id

        # Vérifie que le membre n'a pas déjà 3 emprunts ou d'emprunt en retard
        emprunts_actifs = Emprunt.objects.filter(membre=membre, rendu=False)
        #  Vérifier les retards d’abord
        if any(e.est_en_retard() for e in emprunts_actifs):
            messages.error(request, f'Vous avez un emprunt en retard.')
            return redirect('public:liste_medias')
        if emprunts_actifs.count() >= 3:
            messages.error(request, "Vous avez déjà 3 emprunts en cours. merci de bien vouloir retourner avant d'emprunter de nouveau")
        elif Emprunt.objects.filter(membre=membre, media=media, rendu=False).exists():
            messages.error(request, "Vous avez déjà emprunté ce média.")
        elif not media.disponible:
            messages.error(request, "Ce média n'est plus disponible.")
        else:
            # créer l'emprunt
            Emprunt.objects.create(membre=membre, media=media)
            media.disponible = False
            media.save()
            messages.success(request, f"Vous avez emprunté « {media.titre} » avec succès.")
            return redirect('public:liste_medias')



    # Get : afficher le formulaire, passer membre si déjà en session
    membre = None
    membre_id = request.session.get('membre_id')
    if membre_id:
        membre = get_object_or_404(Membre, pk=membre_id)

    return render(request, 'medias/form_emprunt.html', {'media':media, 'membre': membre})


def retourner_media(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)

    if emprunt.rendu:
        messages.warning(request, f'le média "{emprunt.media.titre}" a déjà été retourné.')
    else:
        emprunt.rendu = True
        emprunt.date_retour = date.today() # si on veut enregistrer la date réelle
        emprunt.save()

        # Remettre le média comme disponible
        media = emprunt.media
        media.disponible = True
        media.save(update_fields=['disponible'])  # <- important pour que ça s'enregistre
        media.refresh_from_db()  # rafraîchir si tu l'utilises après

        messages.success(request, f'Vous avez retourné "{emprunt.media.titre}". merci !')

    return redirect('public:liste_medias')



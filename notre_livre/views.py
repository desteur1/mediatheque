from django.shortcuts import render, redirect, get_object_or_404
from .models import Media


def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'medias/display.html', {'medias':medias})

def detail_medias(request, id):
    media = get_object_or_404(Media, id=id)
    return render(request, 'medias/detail.html', {'media': media})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Media


def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'medias/display.html', {'medias':medias})




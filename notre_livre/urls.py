from mediatheque.urls import urlpatterns

urlpatterns =[
    path ('', views.liste_medias, name='liste_medias'),
    path ('<int:id>/', views.detail_medias, name='detail_medias'),
]
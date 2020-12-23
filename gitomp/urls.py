from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('boards', include('boards.urls')),
    path('albums', include('albums.urls')),
    path('concerts, include('concerts.urls')),
]


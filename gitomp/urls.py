from django.urls import path, include

urlpatterns = [
  
    path('users', include('users.urls')),
    path('concerts', include('concerts.urls')),
    path('boards', include('boards.urls')),
    path('albums', include('albums.urls')),
    

]


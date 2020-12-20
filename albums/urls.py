from django.urls import path
from albums.views  import ListView, DetailPageView, MainAlbumsView

urlpatterns = [
    path('',ListView.as_view()),
    path('/<int:album_pk>',DetailPageView.as_view()),
    path('/main-page', MainAlbumsView.as_view()),
]

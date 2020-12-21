from django.urls import path
from albums.views  import AlbumListView, AlbumDetailView, AlbumMainView

urlpatterns = [
    path('',AlbumListView.as_view()),
    path('/<int:album_pk>',AlbumDetailView.as_view()),
    path('/main-page', AlbumMainView.as_view()),
]

from django.urls import path
from boards.views import BoardView,BoardDetailView,CommentView

urlpatterns = [
    path('',BoardView.as_view()),
    path('/<int:board_pk>',BoardDetailView.as_view()),
    path('/<int:board_pk>/comments',CommentView.as_view()),
    path('/<int:board_pk>/comments/<int:comment_pk>',CommentView.as_view())
]


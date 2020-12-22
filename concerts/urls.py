from django.urls import path
from concerts.views import ConcertUpcommingView, ConcertListView, ConcertDetailView

urlpatterns = [
    path('/upcomming', ConcertUpcommingView.as_view()),
    path('',ConcertListView.as_view()),
    path('/<int:concert_pk>', ConcertDetailView.as_view())
]


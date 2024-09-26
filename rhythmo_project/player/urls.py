from django.urls import path
from . import views

urlpatterns = [
    path('add_track/', views.add_track, name='add_track'),
    path('', views.track_list, name='track_list'),
    path('tracks/listen/<int:track_id>/', views.listen_track, name='listen_track'),
]
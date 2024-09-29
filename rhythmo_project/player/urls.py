from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ArtistViewSet, GenreViewSet, AlbumViewSet, TrackViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = [
    path('add_track/', views.add_track, name='add_track'),
    path('', views.track_list, name='track_list'),
    path('api/', include(router.urls)),
    path('tracks/listen/<int:track_id>/', views.listen_track, name='listen_track'),
]
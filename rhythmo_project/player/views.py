from django.shortcuts import render, redirect
from .models import User, Artist, Genre, Album, Track, Playlist
from .forms import TrackForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets
from .services import TrackService
from .serializers import (
    UserSerializer, ArtistSerializer, GenreSerializer,
    AlbumSerializer, TrackSerializer, PlaylistSerializer
)
from .services import (
    UserService, ArtistService, GenreService,
    AlbumService, TrackService, PlaylistService
)


#@login_required
def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            TrackService.add_track(form, request.user)
            return redirect('track_list')
    else:
        form = TrackForm()

    return render(request, 'player/add_track.html', {'form': form})


#@login_required
def track_list(request):
    tracks = TrackService.get_all_tracks()
    return render(request, 'player/track_list.html', {'tracks': tracks})


#@login_required
def listen_track(request, track_id):
    track = TrackService.get_track_by_id(track_id)

    #TrackService.log_listening_history(request.user, track)

    return render(request, 'player/listen_track.html', {'track': track})


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserService.get_all_users()
    serializer_class = UserSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = ArtistService.get_all_artists()
    serializer_class = ArtistSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = GenreService.get_all_genres()
    serializer_class = GenreSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = AlbumService.get_all_albums()
    serializer_class = AlbumSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = TrackService.get_all_tracks()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = PlaylistService.get_all_playlists()
    serializer_class = PlaylistSerializer
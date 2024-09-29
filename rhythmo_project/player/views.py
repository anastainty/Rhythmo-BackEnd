from django.shortcuts import render, redirect
from .models import User, Artist, Genre, Album, Track, Playlist
from .serializers import UserSerializer, ArtistSerializer, GenreSerializer, AlbumSerializer, TrackSerializer, PlaylistSerializer
from .forms import TrackForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets


@login_required
def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('track_list')
    else:
        form = TrackForm()

    return render(request, 'player/add_track.html', {'form': form})


@login_required
def track_list(request):
    tracks = Track.objects.all()
    return render(request, 'player/track_list.html', {'tracks': tracks})


@login_required
def listen_track(request, track_id):
    track = Track.objects.get(id=track_id)

    #ListeningHistory.objects.create(user=request.user, track=track, listened_at=timezone.now())

    return render(request, 'player/listen_track.html', {'track': track})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
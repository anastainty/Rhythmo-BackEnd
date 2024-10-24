from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .forms import TrackForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import (
    UserSerializer, ArtistSerializer, GenreSerializer,
    AlbumSerializer, TrackSerializer, PlaylistSerializer
)
from .services import (
    UserService, ArtistService, GenreService,
    AlbumService, TrackService, PlaylistService
)
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm
from rest_framework_simplejwt.tokens import RefreshToken
from .services import verify_and_refresh_tokens, RegistrationService


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
    response = verify_and_refresh_tokens(request)
    if response is True:
        return render(request, 'player/track_list.html', {'tracks': tracks})
    return response

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = redirect('track_list')
            response.set_cookie('access', str(refresh.access_token))
            response.set_cookie('refresh', str(refresh))
            return response
    else:
        form = UserLoginForm()
    return render(request, 'player/login.html', {'form': form})


#@login_required
def listen_track(request, track_id):
    track = TrackService.get_track_by_id(track_id)
    response = verify_and_refresh_tokens(request)
    if response is True:
        # TrackService.log_listening_history(request.user, track)
        return render(request, 'player/listen_track.html', {'track': track})
    return response

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            RegistrationService.send_verification_email(request, user)

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'player/register.html', {'form': form})


# Activation view that delegates to services to activate user
def activate_view(request, uid, token):
    if RegistrationService.activate_user(uid, token):  # Delegate to service
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserService.get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = ArtistService.get_all_artists()
    serializer_class = ArtistSerializer
    permission_classes = (IsAuthenticated,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = GenreService.get_all_genres()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = AlbumService.get_all_albums()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated,)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = TrackService.get_all_tracks()
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = PlaylistService.get_all_playlists()
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated,)

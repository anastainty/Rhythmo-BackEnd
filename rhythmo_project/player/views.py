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
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserRegisterForm, UserLoginForm
from rest_framework_simplejwt.tokens import RefreshToken
from .services import verify_and_refresh_tokens, RegistrationService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.shortcuts import get_object_or_404
from .models import User, Playlist, PlaylistTrack, Track, Artist, Album
from PIL import Image
from io import BytesIO
import base64


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


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.is_active = False
            user.save()

            RegistrationService.send_verification_email(request, user)

            return Response({"message": "User registered successfully. Please check your email for verification."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryTracksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def resize_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img = img.resize((50, 50))  # Resize to 50x50
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                buffer.seek(0)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            return None  # Handle missing or invalid images

    def get(self, request, username):
        if request.user.username != username:
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, username=username)

        playlist = Playlist.objects.filter(user=user, name="library").first()
        if not playlist:
            return Response({"detail": "Library playlist not found."}, status=status.HTTP_404_NOT_FOUND)

        playlist_tracks = PlaylistTrack.objects.filter(playlist=playlist).select_related('track')
        tracks = [pt.track for pt in playlist_tracks]

        # Serialize tracks and add resized covers
        serializer = TrackSerializer(tracks, many=True)
        serialized_data = serializer.data

        for track_data, track in zip(serialized_data, tracks):
            if track.cover:  # Assuming `track.cover` is the path to the cover image
                resized_cover = self.resize_image(track.cover.path)
                if resized_cover:
                    track_data['cover'] = resized_cover
            else:
                track_data['cover'] = None

        return Response(serialized_data, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    def resize_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img = img.resize((50, 50))  # Resize to 50x50
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                buffer.seek(0)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            return None  # Handle missing or invalid images

    def post(self, request):
        query = request.data.get('query', '')
        type_ = request.data.get('type', 'All')

        results = []

        # Example: search tracks
        if type_ in ['All', 'Songs']:
            tracks = Track.objects.filter(title__icontains=query)
            for track in tracks:
                resized_cover = None
                if track.cover:
                    resized_cover = self.resize_image(track.cover.path)

                results.append({
                    'type': 'Track',
                    'id': track.id,
                    'title': track.title,
                    'cover': resized_cover,  # Use resized image here
                    'file': track.file.url if track.file else None,
                    'details': f'Album: {track.album.title if track.album else "N/A"}',
                })

        if type_ in ['All', 'Playlists']:
            playlists = Playlist.objects.filter(name__icontains=query)
            for playlist in playlists:
                resized_cover = None
                if playlist.cover:  # Assuming playlist has a `cover` field
                    resized_cover = self.resize_image(playlist.cover.path)

                results.append({
                    'type': 'Playlist',
                    'id': playlist.id,
                    'name': playlist.name,
                    'cover': resized_cover,
                    'details': f'Created by: {playlist.user.username}',
                })

            # Search Artists
        if type_ in ['All', 'Artists']:
            artists = Artist.objects.filter(name__icontains=query)
            for artist in artists:
                resized_cover = None
                if artist.photo:
                    resized_cover = self.resize_image(artist.photo.path)

                results.append({
                    'type': 'Artist',
                    'id': artist.id,
                    'name': artist.name,
                    'cover': resized_cover,
                })

            # Search Albums
        if type_ in ['All', 'Albums']:
            albums = Album.objects.filter(title__icontains=query)
            for album in albums:
                resized_cover = None
                if album.cover:  # Assuming album has a `cover` field
                    resized_cover = self.resize_image(album.cover.path)

                results.append({
                    'type': 'Album',
                    'id': album.id,
                    'title': album.title,
                    'cover': resized_cover,
                    'details': f'Artist: {album.artist.name if album.artist else "N/A"}',
                })


        return Response(results, status=status.HTTP_200_OK)

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

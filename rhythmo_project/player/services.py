from .models import Track, ListeningHistory
from django.utils import timezone
from .models import User, Artist, Genre, Album, Track, Playlist
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import requests
from django.shortcuts import redirect
from django.core.mail import send_mail
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from itsdangerous import SignatureExpired, BadSignature
from django.contrib.auth import get_user_model

class TrackService:
    @staticmethod
    def add_track(form_data, user):
        """
        Handles the creation of a new track.
        """
        form_data.save()

    @staticmethod
    def get_all_tracks():
        """
        Returns all tracks.
        """
        return Track.objects.all()

    @staticmethod
    def get_track_by_id(track_id):
        """
        Returns a single track by its ID.
        """
        return Track.objects.get(id=track_id)

    @staticmethod
    def log_listening_history(user, track):
        """
        Logs the track listening history for a user.
        """
        ListeningHistory.objects.create(user=user, track=track, listened_at=timezone.now())



class UserService:
    @staticmethod
    def get_all_users():
        user = get_user_model()
        return user.objects.all()

class ArtistService:
    @staticmethod
    def get_all_artists():
        return Artist.objects.all()

class GenreService:
    @staticmethod
    def get_all_genres():
        return Genre.objects.all()

class AlbumService:
    @staticmethod
    def get_all_albums():
        return Album.objects.all()


class PlaylistService:
    @staticmethod
    def get_all_playlists():
        return Playlist.objects.all()

def verify_and_refresh_tokens(request):
    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')

    if access_token:
        try:
            # Verify the access token
            AccessToken(access_token)
            return True  # Access token is valid

        except TokenError:
            # Access token is expired, attempt to refresh using refresh token
            if refresh_token:
                try:
                    response = requests.post(
                        f"{request.scheme}://{request.get_host()}/api/token/refresh/",
                        data={'refresh': refresh_token}
                    )
                    if response.status_code == 200:
                        new_access_token = response.json().get('access')
                        response = redirect('main')
                        response.set_cookie('access', new_access_token)
                        return response  # Return updated response with refreshed token
                    else:
                        # Refresh token failed, redirect to login
                        return redirect('login')
                except Exception:
                    return redirect('login')
            else:
                # No refresh token, redirect to login
                return redirect('login')
    else:
        # No access token, redirect to login
        return redirect('login')

def generate_token(user):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(user.email, salt=settings.SECRET_KEY)

class RegistrationService:

    def send_verification_email(request, user):
        token = generate_token(user)
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('player/verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': user.pk,
            'token': token,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    # Function to activate user account based on the verification token
    def activate_user(uid, token):
        try:
            user = User.objects.get(pk=uid)
            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            email = serializer.loads(token, salt=settings.SECRET_KEY, max_age=3600)
            if user.email == email:
                user.is_active = True
                user.save()
                return True
            return False
        except (BadSignature, User.DoesNotExist):
            return False
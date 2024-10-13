from .models import Track, ListeningHistory
from django.utils import timezone
from .models import User, Artist, Genre, Album, Track, Playlist


class TrackService:
    @staticmethod
    def add_track(form_data, user):
        """
        Handles the creation of a new track.
        """
        form_data.save()

    @staticmethod
    def get_track_list():
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
        return User.objects.all()

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

class TrackService:
    @staticmethod
    def get_all_tracks():
        return Track.objects.all()

class PlaylistService:
    @staticmethod
    def get_all_playlists():
        return Playlist.objects.all()
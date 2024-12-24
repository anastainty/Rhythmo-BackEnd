from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from decouple import config

class User(AbstractUser):
    password = models.CharField(max_length=255, default=make_password(config('DEFAULT_PASSWORD')))
    avatar_path = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.username

class Artist(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Track(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    cover = models.ImageField(upload_to='tracks/', blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    file = models.FileField(upload_to='songs/', null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    cover = models.ImageField(upload_to='playlists/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.playlist.name} - {self.track.title}'

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.track.title}'

class ArtistGenre(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('artist', 'genre')


class ArtistTrack(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('artist', 'track')


class UserAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'album')


class ArtistAlbum(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('artist', 'album')


class PlaylistGenre(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playlist', 'genre')


class ArtistFollower(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('artist', 'user')
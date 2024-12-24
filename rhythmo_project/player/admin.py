from django.contrib import admin
from .models import User, Artist, Genre, Album, Track, Playlist, PlaylistTrack, ListeningHistory, ArtistTrack

admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(ListeningHistory)
admin.site.register(ArtistTrack)
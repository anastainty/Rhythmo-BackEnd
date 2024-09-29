from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Artist, Genre, Album, Track, Playlist
class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password_hash': 'hashed_password',
            'avatar_path': 'path/to/avatar.jpg'
        }

    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_read_users(self):
        User.objects.create(**self.user_data)
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_user(self):
        user = User.objects.create(**self.user_data)
        url = reverse('user-detail', args=[user.id])
        updated_data = {'username': 'updateduser'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, 'updateduser')

    def test_delete_user(self):
        user = User.objects.create(**self.user_data)
        url = reverse('user-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class ArtistTests(APITestCase):

    def test_create_artist(self):
        url = reverse('artist-list')
        data = {'name': 'Test Artist', 'bio': 'This is a test artist.', 'avatar_path': 'path/to/avatar.jpg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.get().name, 'Test Artist')

    def test_get_artist_list(self):
        Artist.objects.create(name='Test Artist', bio='This is a test artist.')
        url = reverse('artist-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_artist_detail(self):
        artist = Artist.objects.create(name='Test Artist', bio='This is a test artist.')
        url = reverse('artist-detail', kwargs={'pk': artist.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Artist')

    def test_update_artist(self):
        artist = Artist.objects.create(name='Test Artist', bio='This is a test artist.')
        url = reverse('artist-detail', kwargs={'pk': artist.pk})
        data = {'name': 'Updated Artist', 'bio': 'Updated bio'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        artist.refresh_from_db()
        self.assertEqual(artist.name, 'Updated Artist')

    def test_delete_artist(self):
        artist = Artist.objects.create(name='Test Artist')
        url = reverse('artist-detail', kwargs={'pk': artist.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Artist.objects.count(), 0)

class AlbumTests(APITestCase):

    def test_create_album(self):
        url = reverse('album-list')
        data = {'title': 'Test Album', 'release_date': '2024-01-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(Album.objects.get().title, 'Test Album')

    def test_get_album_list(self):
        Album.objects.create(title='Test Album')
        url = reverse('album-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_album_detail(self):
        album = Album.objects.create(title='Test Album')
        url = reverse('album-detail', kwargs={'pk': album.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Album')

    def test_update_album(self):
        album = Album.objects.create(title='Test Album')
        url = reverse('album-detail', kwargs={'pk': album.pk})
        data = {'title': 'Updated Album'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        album.refresh_from_db()
        self.assertEqual(album.title, 'Updated Album')

    def test_delete_album(self):
        album = Album.objects.create(title='Test Album')
        url = reverse('album-detail', kwargs={'pk': album.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)

class TrackTests(APITestCase):

    def test_create_track(self):
        album = Album.objects.create(title='Test Album')
        genre = Genre.objects.create(name='Rock')
        url = reverse('track-list')
        data = {
            'title': 'Test Track',
            'album_id': album.id,
            'genre_id': genre.id,
            'duration': '00:03:30',
            'release_date': '2024-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 1)
        self.assertEqual(Track.objects.get().title, 'Test Track')

    def test_get_track_list(self):
        Track.objects.create(title='Test Track')
        url = reverse('track-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_track_detail(self):
        track = Track.objects.create(title='Test Track')
        url = reverse('track-detail', kwargs={'pk': track.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Track')

    def test_update_track(self):
        track = Track.objects.create(title='Test Track')
        url = reverse('track-detail', kwargs={'pk': track.pk})
        data = {'title': 'Updated Track'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        track.refresh_from_db()
        self.assertEqual(track.title, 'Updated Track')

    def test_delete_track(self):
        track = Track.objects.create(title='Test Track')
        url = reverse('track-detail', kwargs={'pk': track.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Track.objects.count(), 0)

class PlaylistTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password_hash='testpassword')

    def test_get_playlist_list(self):
        Playlist.objects.create(name='Test Playlist', user=self.user)
        url = reverse('playlist-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_playlist_detail(self):
        playlist = Playlist.objects.create(name='Test Playlist', user=self.user)
        url = reverse('playlist-detail', kwargs={'pk': playlist.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Playlist')

    def test_update_playlist(self):
        playlist = Playlist.objects.create(name='Test Playlist', user=self.user)
        url = reverse('playlist-detail', kwargs={'pk': playlist.pk})
        data = {'name': 'Updated Playlist'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        playlist.refresh_from_db()
        self.assertEqual(playlist.name, 'Updated Playlist')

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(name='Test Playlist', user=self.user)
        url = reverse('playlist-detail', kwargs={'pk': playlist.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)
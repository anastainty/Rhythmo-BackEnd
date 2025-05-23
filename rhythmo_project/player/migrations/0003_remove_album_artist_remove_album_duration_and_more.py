# Generated by Django 5.1.1 on 2024-09-29 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_remove_track_file_path_track_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='album',
            name='duration',
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.CreateModel(
            name='ArtistAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.artist')),
            ],
            options={
                'unique_together': {('artist', 'album')},
            },
        ),
        migrations.CreateModel(
            name='ArtistFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.user')),
            ],
            options={
                'unique_together': {('artist', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ArtistGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.artist')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.genre')),
            ],
            options={
                'unique_together': {('artist', 'genre')},
            },
        ),
        migrations.CreateModel(
            name='ArtistTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.artist')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.track')),
            ],
            options={
                'unique_together': {('artist', 'track')},
            },
        ),
        migrations.CreateModel(
            name='PlaylistGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.genre')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.playlist')),
            ],
            options={
                'unique_together': {('playlist', 'genre')},
            },
        ),
        migrations.CreateModel(
            name='UserAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.user')),
            ],
            options={
                'unique_together': {('user', 'album')},
            },
        ),
    ]

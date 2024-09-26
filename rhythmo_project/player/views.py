from django.shortcuts import render, redirect
from .models import Track, ListeningHistory
from .forms import TrackForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
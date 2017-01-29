from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Genre, Track
import requests


def home(request):
    #    get_genres()
    #    get_tracks()
    return render(request, 'tracks/content_page.html', {})


def tracks_list(request):
    track_list = Track.objects.all()
    paginator = Paginator(track_list, 10)
    page = request.GET.get('page', 1)

    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        tracks = paginator.page(1)
    except EmptyPage:
        tracks = paginator.page(paginator.num_pages)

    return render(request, 'tracks/track_list.html', {'tracks': tracks})


def add_track(request):
    return HttpResponse("Add Tracks")


def this_track(request, track_id):
    return HttpResponse("This Track")


def edit_track(request, track_id):
    return HttpResponse("Edit Track")


def genres_list(request):
    genre_list = Genre.objects.all()
    paginator = Paginator(genre_list, 10)
    page = request.GET.get('page', 1)

    try:
        genres = paginator.page(page)
    except PageNotAnInteger:
        genres = paginator.page(1)
    except EmptyPage:
        genres = paginator.page(paginator.num_pages)

    return render(request, 'tracks/genre_list.html', {'genres': genres})


def add_genre(request):
    return HttpResponse("Add Genres")


def this_genre(request, genre_id):
    return HttpResponse("This Genre")


def edit_genre(request, genre_id):
    return HttpResponse("Edit Genre")


def get_genres(url='http://104.197.128.152:8000/v1/genres'):
    r = requests.get(url)
    genres = r.json()

    for genre in genres['results']:
        Genre.objects.get_or_create(genre_id=genre['id'], genre_type=genre['name'])

    if genres['next']:
        get_genres(genres['next'])


def get_tracks(url='http://104.197.128.152:8000/v1/tracks'):
    r = requests.get(url)
    songs = r.json()

    for song in songs['results']:
        obj, created = Track.objects.get_or_create(title_id=song['id'], title=song['title'], rating=song['rating'])
        if song['genres']:
            for genre_item in song['genres']:
                Genre.objects.get_or_create(genre_id=genre_item['id'], genre_type=genre_item['name'])
                obj.genre.add(Genre.objects.get(genre_id=genre_item['id']))

    if songs['next']:
        get_tracks(songs['next'])

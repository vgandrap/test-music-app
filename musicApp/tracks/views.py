from django.shortcuts import render
from django.http import HttpResponse
from .models import Genre, Track

def all_tracks(request):
    get_tracks()
    return render(request, 'tracks/base.html', {})

def add_track(request):
    return HttpResponse("Add Tracks")

def this_track(request, track_id):
    return HttpResponse("This Track")

def edit_track(request, track_id):
    return HttpResponse("Edit Track")

def all_genres(request):
    return HttpResponse("All Genres")

def add_genre(request):
    return HttpResponse("Add Genres")

def this_genre(request, genre_id):
    return HttpResponse("This Genre")

def edit_genre(request, genre_id):
    return HttpResponse("Edit Genre")

def get_genres(url='http://104.197.128.152:8000/v1/genres'):
    r=requests.get(url)
    genres=r.json()

    for genre in genres['results']:
        obj, created = Genre.objects.get_or_create(genre_id=genre['id'], genre_type=genre['name'])

    if genres['next']:
        get_genres(genres['next'])

def get_tracks(url='http://104.197.128.152:8000/v1/tracks'):
    r=requests.get(url)
    songs=r.json()

    for song in songs['results']:
        obj, created = Track.objects.get_or_create(title_id=song['id'], title=song['title'], rating=song['rating'])
        if song['genres']:
            for genre_item in song['genres']:
                gen_obj, gen_created = Genre.objects.get_or_create(genre_id=genre_item['id'], genre_type=genre_item['name'])
                obj.genre.add(Genre.objects.get(genre_id=genre_item['id']))

    if songs['next']:
        get_tracks(songs['next'])

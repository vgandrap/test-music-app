from django.shortcuts import render
from django.http import HttpResponse

def all_tracks(request):
    return HttpResponse("All Tracks")

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
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Genre, Track
from .decorators import run_once
import urllib
import json


def home(request):
    status = 500
    response_to_frontend = {'message': 'Error Loading the page details'}
    try:
        return render(request, 'tracks/content_page.html')
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def tracks_list(request):
    status = 500
    response_to_frontend = {'message': 'Cound not load tracks'}
    try:
        get_tracks()
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
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def add_track(request):
    status = 500
    if request.POST:
        response_to_frontend = {'message': 'Unable to add track'}
        parameters = {}

        for item in request.POST:
            try:
                parameters = json.loads(item)
            except:
                pass

        json_data = {'title': parameters['track_title'], 'rating': parameters['track_rating'], 'genres': []}
        if parameters.get('track_genre'):
            for genre in parameters['track_genre']:
                json_data['genres'].append(genre['id'])

        api_url_path = 'http://104.197.128.152:8000/v1/tracks'

        try:
            json_headers = {'content-type': 'application/json'}
            json_response = requests.post(
                api_url_path,
                data=json.dumps(json_data),
                headers=json_headers
            )

            status = json_response.status_code
            json_object = json_response.json()
            if json_object.get('reason'):
                response_to_frontend['message'] = json_object['reason']
            else:
                response_to_frontend['message'] = json_object['rating']
            if json_response.status_code == 200:
                response_to_frontend['status_code'] = json_response.status_code
                if json_object.get('id'):
                    response_to_frontend['id'] = json_object['id']
                    obj, created = Track.objects.update_or_create(title_id=json_object['id'], title=json_data['title'],
                                                                  rating=json_data['rating'])
                    if json_data['genres']:
                        for genre_item in json_data['genres']:
                            obj.genre.add(Genre.objects.get(genre_id=genre_item['id']))

        except:
            pass

        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )

    return


def track_search(request):
    status = 500
    response_to_frontend = {'message': 'Could not find tracks matching the query'}
    try:
        query = urllib.quote(request.GET.get('query').encode('utf8'))

        search_url = 'http://104.197.128.152:8000/v1/tracks?title=' + query

        r = requests.get(search_url)
        results = r.json()

        track_results = []

        for song in results['results']:
            obj = {'title_id': song['id'], 'title': song['title'], 'rating': song['rating'], 'genre': []}
            if song['genres']:
                for genre_item in song['genres']:
                    g = {'genre_id': genre_item['id'], 'genre_type': genre_item['name']}
                    obj['genre'].append(g)
            track_results.append(obj)

        if results['next']:
            get_tracks(results['next'])

        paginator = Paginator(track_results, 10)
        page = request.GET.get('page', 1)

        try:
            tracks = paginator.page(page)
        except PageNotAnInteger:
            tracks = paginator.page(1)
        except EmptyPage:
            tracks = paginator.page(paginator.num_pages)

        return render(request, 'tracks/modal/search_result_modal.html', {'search_results': tracks})
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def this_track(request, track_id):
    status = 500
    response_to_frontend = {'message': 'Could not find specified track details'}
    try:
        track_object = Track.objects.get(title_id=track_id)
        track_details = {'track_id': track_object.title_id, 'title': track_object.title, 'rating': track_object.rating}
        genres = []
        for g_item in track_object.genre.all():
            g = {'genre_title': g_item.genre_type, 'genre_id': g_item.genre_id}
            genres.append(g)

        track_details['genre'] = genres

        return JsonResponse(track_details)
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def edit_track(request, track_id):
    status = 500
    if request.POST:
        response_to_frontend = {'message': 'Could not edit track'}
        parameters = {}

        for item in request.POST:
            try:
                parameters = json.loads(item)
            except:
                pass

        json_data = {'id': parameters['track_id'], 'title': parameters['track_title'],
                     'rating': parameters['track_rating'], 'genres': []}
        if parameters.get('track_genre'):
            for genre in parameters['track_genre']:
                json_data['genres'].append(genre['id'])

        api_url_path = 'http://104.197.128.152:8000/v1/tracks/' + track_id

        try:
            json_headers = {'content-type': 'application/json'}
            json_response = requests.post(
                api_url_path,
                data=json.dumps(json_data),
                headers=json_headers
            )

            status = json_response.status_code
            json_object = json_response.json()
            if json_object.get('reason'):
                response_to_frontend['message'] = json_object['reason']
            else:
                response_to_frontend['message'] = json_object['rating']
            if json_response.status_code == 200:
                response_to_frontend['status_code'] = json_response.status_code

                if json_object.get('id'):
                    response_to_frontend['id'] = json_object['id']
                    obj, created = Track.objects.update_or_create(title_id=json_data['id'], title=json_data['title'],
                                                                  rating=json_data['rating'])
                    if json_data['genres']:
                        for genre_item in json_data['genres']:
                            obj.genre.add(Genre.objects.get(genre_id=genre_item['id']))

        except:
            pass

        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )

    return


def genres_list(request):
    status = 500
    response_to_frontend = {'message': 'Unable to load all genres'}
    try:
        get_genres()
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
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def add_genre(request):
    status = 500
    if request.POST:
        response_to_frontend = {'message': 'Unable to add genre'}
        parameters = {}

        for item in request.POST:
            try:
                parameters = json.loads(item)
            except:
                pass

        json_data = {'name': parameters['genre_type']}

        api_url_path = 'http://104.197.128.152:8000/v1/genres'

        try:
            json_headers = {'content-type': 'application/json'}
            json_response = requests.post(
                api_url_path,
                data=json.dumps(json_data),
                headers=json_headers
            )

            status = json_response.status_code
            json_object = json_response.json()
            if json_object.get('reason'):
                response_to_frontend['message'] = json_object['reason']
            if json_response.status_code == 200:
                response_to_frontend['status_code'] = json_response.status_code

                if json_object.get('id'):
                    response_to_frontend['id'] = json_object['id']
                    Genre.objects.update_or_create(genre_id=json_object['id'], genre_type=json_data['name'])

        except:
            pass

        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )

    return


def this_genre(request, genre_id):
    status = 500
    response_to_frontend = {'message': 'Could not find specified track details'}
    try:
        genre_object = Genre.objects.get(genre_id=genre_id)
        genre_details = {'genre_id': genre_object.genre_id, 'title': genre_object.genre_type}
        return JsonResponse(genre_details)
    except:
        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )


def edit_genre(request, genre_id):
    status = 500
    if request.POST:
        response_to_frontend = {'message': 'Could not edit genre'}
        parameters = {}

        for item in request.POST:
            try:
                parameters = json.loads(item)
            except:
                pass

        json_data = {'id': parameters['genre_id'], 'name': parameters['track_title']}

        api_url_path = 'http://104.197.128.152:8000/v1/genres' + genre_id

        try:
            json_headers = {'content-type': 'application/json'}
            json_response = requests.post(
                api_url_path,
                data=json.dumps(json_data),
                headers=json_headers
            )

            status = json_response.status_code
            json_object = json_response.json()
            if json_object.get('reason'):
                response_to_frontend['message'] = json_object['reason']
            if json_response.status_code == 200:
                response_to_frontend['status_code'] = json_response.status_code

                if json_object.get('id'):
                    response_to_frontend['id'] = json_object['id']
                    Genre.objects.update_or_create(genre_id=json_data['id'], genre_type=json_data['name'])

        except:
            pass

        return HttpResponse(
            json.dumps(response_to_frontend),
            status=status,
            content_type='application/json'
        )

    return


@run_once
def get_genres(url='http://104.197.128.152:8000/v1/genres'):
    r = requests.get(url)
    genres = r.json()

    for genre in genres['results']:
        Genre.objects.update_or_create(genre_id=genre['id'], genre_type=genre['name'])

    if genres['next']:
        get_genres(genres['next'])


@run_once
def get_tracks(url='http://104.197.128.152:8000/v1/tracks'):
    r = requests.get(url)
    songs = r.json()

    for song in songs['results']:
        obj, created = Track.objects.update_or_create(title_id=song['id'], title=song['title'], rating=song['rating'])
        if song['genres']:
            for genre_item in song['genres']:
                Genre.objects.update_or_create(genre_id=genre_item['id'], genre_type=genre_item['name'])
                obj.genre.add(Genre.objects.get(genre_id=genre_item['id']))

    if songs['next']:
        get_tracks(songs['next'])

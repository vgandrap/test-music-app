from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^track_list/?$', views.tracks_list, name='tracks_list'),
    url(r'^add/?$', views.add_track, name='add_tracks'),
    url(r'^(?P<track_id>[0-9]+)/?$', views.this_track, name='track'),
    url(r'^(?P<track_id>[0-9]+)/edit/?$', views.edit_track, name='edit_track'),
    url(r'^genre/?$', views.genres_list, name='genres_list'),
    url(r'^genre/add?$', views.add_genre, name='add_genre'),
    url(r'^genre/(?P<genre_id>[0-9]+)/?$', views.this_genre, name='genre'),
    url(r'^genre/(?P<genre_id>[0-9]+)/edit/?$', views.edit_genre, name='edit_genre'),
]
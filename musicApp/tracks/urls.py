from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_tracks, name='all_tracks'),
    url(r'^add/?$', views.add_track, name='add_tracks'),
    url(r'^(?P<track_id>[0-9]+)/?$', views.this_track, name='track'),
    url(r'^(?P<track_id>[0-9]+)/edit/?$', views.edit_track, name='edit_track'),
    url(r'^genre/?$', views.all_genres, name='all_genres'),
    url(r'^genre/add?$', views.add_genre, name='add_genre'),
    url(r'^genre/(?P<genre_id>[0-9]+)/?$', views.this_genre, name='genre'),
    url(r'^genre/(?P<genre_id>[0-9]+)/edit/?$', views.edit_genre, name='edit_genre'),
]
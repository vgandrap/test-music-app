from django.contrib import admin

from .models import Track
from .models import Genre

admin.site.register(Track)
admin.site.register(Genre)
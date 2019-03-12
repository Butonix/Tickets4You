from django.urls import re_path

from .views import profile

app_name = 'users'
urlpatterns = [
    re_path(r'^$', profile, name='profile'),
]

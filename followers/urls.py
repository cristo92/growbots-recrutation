from django.conf.urls import url

from . import views
from . import json


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/ajax/update_followers.json$', json.provide_second_followers, name='provide_second_followers'),
    url(r'^/(?P<user_id>[0-9]+)/get_followers.json$', json.get_followers_json, name='get_followers_json'),
]


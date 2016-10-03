from django.conf.urls import url

from . import views
from . import ajax


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/ajax/update.json$', ajax.provide_data, name='provide_data'),
    url(r'^/ajax/update_followers.json$', ajax.provide_second_followers, name='provide_second_followers'),
]


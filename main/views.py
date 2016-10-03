from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import tweepy

def index(request):
    template = loader.get_template('main/index.html')

    consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
    consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    
    context = {}
    if(request.session.get('access_token', None) and request.session.get('access_token_secret', None)):
        # TODO create generiz url
        #context = { "authorization_url": "https://localhost:8000/followers/followers", "auth": auth }
        context = { "authorization_url": "https://still-retreat-54855.herokuapp.com/followers/followers", "auth": auth }
    else:
        context = { "authorization_url": auth.get_authorization_url(), "auth": auth }
        request.session['request_token'] = auth.request_token

    return HttpResponse(template.render(context, request))
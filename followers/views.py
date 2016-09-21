from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import tweepy

def index(request):
    template = loader.get_template('followers/index.html')
    llist = [i for i in range(0, 10)]

    #get oauth from GET
    consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
    consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"
    request_token=request.session.get('request_token', None)
    verifier_token=request.GET.get('oauth_verifier', None)

    context = { 
        'basic_list': llist, 
        'name': None
    }

    if(request_token and verifier_token):

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, "http://localhost:8000/followers/followers")
        auth.secure = True
        auth.request_token = request_token

        auth.get_access_token(verifier_token)

        api = tweepy.API(auth)

        context['name'] = api.me().name

    return HttpResponse(template.render(context, request))

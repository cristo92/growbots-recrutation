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

    access_token = request.session.get('access_token', None)
    access_token_secret = request.session.get('access_token_secret', None)

    request_token=request.session.get('request_token', None)
    verifier_token=request.GET.get('oauth_verifier', None)

    context = { 
        'basic_list': llist, 
        'name': None,
        'friends': []
    }

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True

    api = None

    if(access_token and access_token_secret):
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

    elif(request_token and verifier_token):
        auth.request_token = request_token

        auth.get_access_token(verifier_token)

        request.session['access_token'] = auth.access_token
        request.session['access_token_secret'] = auth.access_token_secret

        api = tweepy.API(auth)
    
    if(api):
        username = auth.get_username()
        context['name'] = api.me().name

        friends = api.friends_ids(username)
        context['friends'] = [api.get_user(x).screen_name for x in friends]

    return HttpResponse(template.render(context, request))

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
    
    context = { "authorization_url": auth.get_authorization_url() }

    request.session['request_token'] = auth.request_token

    return HttpResponse(template.render(context, request))

def oauthorize():
    # == OAuth Authentication ==
    consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
    consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

    access_token="l-gh6QAAAAAAxFSnAAABV05F_V8"
    access_token_secret="QLmp2CbpVkB27lZf5IjisjRabJdsw8EY"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    print auth.get_authorization_url()


    auth.get_access_token("verifier_value")


    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    print(api.me().name)

    api.update_status(status='Updating using OAuth authentication via Tweepy!')

def oauthorize2():
    # == OAuth Authentication ==
    consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
    consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

    request_token="l-gh6QAAAAAAxFSnAAABV05F_V8"
    verifier="QLmp2CbpVkB27lZf5IjisjRabJdsw8EY"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    print auth.get_authorization_url()
    auth.request_token=request_token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
        return None

    auth.set_access_token(auth.access_token, auth.access_token_secret)

    api = tweepy.API(auth)

    print(api.me().name)

    api.update_status(status='Updating using OAuth authentication via Tweepy!')
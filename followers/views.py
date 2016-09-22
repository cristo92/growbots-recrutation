from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from functional import foldl

import tweepy

def authorize(request):
    """ Returns api """
    consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
    consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

    access_token = request.session.get('access_token', None)
    access_token_secret = request.session.get('access_token_secret', None)

    request_token=request.session.get('request_token', None)
    verifier_token=request.GET.get('oauth_verifier', None)

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

    return api

FRIENDS_PER_REQUEST = 1

def index(request):
    template = loader.get_template('followers/index.html')
    llist = range(0, 10)

    upk = 12314215

    context = { 
        'basic_list': llist, 
        'name': None,
        'friends': [],
        'pk': upk
    }

    request.session['pk'] = upk
    
    api = authorize(request)

    if(api):
        username = api.me().name
        context['name'] = username

        friends_ids = api.friends_ids(username)
        friends = api.lookup_users(user_ids=friends_ids)

        context['friends'] = [(x.screen_name, x.profile_image_url) for x in friends]
        request.session['friends'] = friends_ids[FRIENDS_PER_REQUEST:]

        #TODO don't override limits
        snd_friends_ids = foldl(lambda x, y: x + y, [], [api.friends_ids(id=x) for x in friends_ids[:FRIENDS_PER_REQUEST]])
        snd_friends = []
        while snd_friends_ids:
            snd_friends += api.lookup_users(user_ids=snd_friends_ids[:100])
            del snd_friends_ids[:100]

        context['snd_friends'] = [(x.screen_name, x.profile_image_url) for x in snd_friends]

    return HttpResponse(template.render(context, request))

def additional_content(request, pk):
    template = loader.get_template('followers/more.html')

    friends_ids = request.session.get('friends', None)

    print dir(request.session)

    context = {
        'pk': pk,
        'snd_friends': [],
    }

    if(friends_ids):
        api = authorize(request)
        request.session['friends'] = friends_ids[FRIENDS_PER_REQUEST:]

        #TODO don't override limits
        snd_friends_ids = foldl(lambda x, y: x + y, [], [api.friends_ids(id=x) for x in friends_ids[:FRIENDS_PER_REQUEST]])
        snd_friends = []
        while snd_friends_ids:
            snd_friends += api.lookup_users(user_ids=snd_friends_ids[:100])
            del snd_friends_ids[:100]

        context['snd_friends'] = [(x.screen_name, x.profile_image_url) for x in snd_friends]


    return HttpResponse(template.render(context, request))

"""
    Class User:
        ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', 
        '__getstate__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', 
        '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', 
        '_json', 'contributors_enabled', 'created_at', 'default_profile', 'default_profile_image', 
        'description', 'entities', 'favourites_count', 'follow', 'follow_request_sent', 'followers', 
        'followers_count', 'followers_ids', 'following', 'friends', 'friends_count', 'geo_enabled', 
        'has_extended_profile', 'id', 'id_str', 'is_translation_enabled', 'is_translator', 'lang', 
        'listed_count', 'lists', 'lists_memberships', 'lists_subscriptions', 'location', 'name', 'notifications', 
        'parse', 'parse_list', 'profile_background_color', 'profile_background_image_url', 'profile_background_image_url_https', 
        'profile_background_tile', 'profile_banner_url', 'profile_image_url', 'profile_image_url_https', 'profile_link_color', 
        'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color', 'profile_use_background_image', 
        'protected', 'screen_name', 'status', 'statuses_count', 'time_zone', 'timeline', 'unfollow', 'url', 'utc_offset', 'verified']
"""

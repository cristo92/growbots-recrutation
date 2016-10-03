from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from cache import set_followers, get_followers, get_or_generate, Context

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

def index(request):
    template = loader.get_template('followers/index.html')

    context = { 
        'name': None,
        'my_id': None,
        'followers': [],
    }
    
    api = authorize(request)
    ctx = Context(api, request)
    print request.session

    if(api):
        me = request.session.get('me', None)
        if(not me):
            me = api.me()
        request.session['me'] = me
        context['name'] = me.name
        context['my_id'] = me.id

        followers_ids = get_or_generate(ctx, me.id)
        print followers_ids

        context['followers'] = followers_ids
        request.session['followers'] = followers_ids

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

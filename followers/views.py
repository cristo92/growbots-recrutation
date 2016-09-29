from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from functional import foldl
from cache import set_friends, get_friends

import tweepy

class Context(object):
    def __init__(self, api, request, friends_ids_limit=0):
        self.api = api
        self.request = request
        self.limits = {
            'friends_ids': friends_ids_limit,
            'lookup_users': 160,
        }

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

def get_or_generate(ctx, uid):
    ret = get_friends(uid)
    if ret == None and ctx.limits['friends_ids']:
        try:
            ret = ctx.api.friends_ids(id=uid)
        except tweepy.TweepError as e:
            if(e.reason == "Not authorized."):
                ret = []
            elif(e.reason == "Sorry, that page does not exist."):
                ret = []
            else:
                print e
                ret = []
        set_friends(uid, ret)
        ctx.limits['friends_ids'] -= 1

    return ret

def count_common_friends(ctx, frs_friends, uid):
    try:
        trd_friends = get_or_generate(ctx, uid)
        if trd_friends == None: return -1
        trd_friends = sorted(trd_friends)
        frs_friends = sorted(frs_friends)
    except tweepy.RateLimitError:
        return -1
    c = 0
    frs_iter = iter(frs_friends)
    trd_iter = iter(trd_friends)
    try:
        f = frs_iter.next()
        t = trd_iter.next()
        while(True):
            c += (f == t)
            if(f < t): f = frs_iter.next()
            else: t = trd_iter.next()
    except StopIteration:
        pass

    return c


def index(request):
    template = loader.get_template('followers/index.html')

    context = { 
        'basic_list': range(0, 10), 
        'name': None,
        'friends': [],
    }
    
    api = authorize(request)
    ctx = Context(api, request, int(request.GET.get('limit', 1)))

    if(api):
        me = request.session.get('me', None)
        if(not me):
            me = api.me()
        request.session['me'] = me
        context['name'] = me.name

        friends_ids = get_or_generate(ctx, me.id)

        context['friends'] = friends_ids
        request.session['friends'] = friends_ids

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

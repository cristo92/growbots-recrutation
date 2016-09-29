from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from functional import foldl
from cache import set_friends, get_friends
from django.views.decorators.cache import cache_page

import tweepy

from views import authorize, Context, count_common_friends, get_or_generate

@cache_page(60 * 60)
def provide_data(request):
    print request.session.get('access_token', 'no token :(')
    print request.session.get('access_token_secret', 'no token :(')

    api = authorize(request)
    if not api:
        return JsonResponse({ 'message': 'Session expired.' })

    ctx = Context(api, request, friends_ids_limit=5)

    frs_friends = request.session.get('friends', None)

    print request.POST
    guys = request.POST.getlist('input[]')
    print guys
    ret = {}
    for guy in guys:
        print guy
        try:
            ret[guy] = count_common_friends(ctx, frs_friends, int(guy))
        except tweepy.TweepError as e:
            if(e.reason == "Not authorized."):
                ret[guy] = "Protected."
            elif(e.reason == "Sorry, that page does not exist."):
                ret[guy] = "Removed."
            else:
                print e
    return JsonResponse(ret)

@cache_page(60 * 60)
def provide_second_friends(request):
    api = authorize(request)
    if not api:
        return JsonResponse({ 'message': 'Session expired.' })
    ctx = Context(api, request, friends_ids_limit=5)

    guys = request.POST.getlist('input[]')
    print guys
    ret = {}
    for guy in guys:
        try:
            ids = get_or_generate(ctx, int(guy))
            snd_friends = []
            try:
                while ids:
                    snd_friends += api.lookup_users(user_ids=ids[:100])
                    del ids[:100]
            except tweepy.RateLimitError as e:
                print "Rate limits on lookup_users was overrided."
                print e
            ret[guy] = map(lambda x: [x.id, x.screen_name, x.profile_image_url], snd_friends)
        except tweepy.TweepError as e:
            if(e.reason == "Not authorized."):
                ret[guy] = []
            elif(e.reason == "Sorry, that page does not exist."):
                ret[guy] = []
            else:
                print e
    return JsonResponse(ret)
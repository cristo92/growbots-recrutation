from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from functional import foldl
from cache import set_followers, get_followers
from django.views.decorators.cache import cache_page

import tweepy

from views import authorize, Context, get_or_generate

@cache_page(60 * 60)
def provide_second_followers(request):
    api = authorize(request)
    if not api:
        return JsonResponse({ 'message': 'Session expired.' })
    ctx = Context(api, request, followers_ids_limit=5)

    guys = request.POST.getlist('input[]')
    print guys
    ret = {}
    for guy in guys:
        ids = get_or_generate(ctx, int(guy))
        snd_followers = []
        try:
            while ids:
                # TODO - control number of lookup_users to avoid exceeding limits
                snd_followers += api.lookup_users(user_ids=ids[:100])
                del ids[:100]
        except tweepy.RateLimitError as e:
            # TODO - Don't just print error - we need solution to replay getting information 
            #        about users (i.e. lookup_users) from this point
            print "Rate limits on lookup_users was exeeded."
            print e
        ret[guy] = map(lambda x: { "id": x.id, "name": x.screen_name, "image_url": x.profile_image_url}, snd_followers)

    return JsonResponse(ret)
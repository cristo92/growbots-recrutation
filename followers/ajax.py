from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from functional import foldl
from django.views.decorators.cache import cache_page
from collections import defaultdict

import tweepy

from views import authorize, Context, get_or_generate
from cache import get_user, set_user, get_followers

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

        def get_user_or_generate(uid):
            user = get_user(uid)
            if(user):
                snd_followers.append(user)
                return False
            return True

        ids = filter(get_user_or_generate, ids)
        print ids

        try:
            while ids:
                # TODO - control number of lookup_users to avoid exceeding limits
                more_users = api.lookup_users(user_ids=ids[:100])

                for user in more_users:
                    set_user(user.id, user)
                snd_followers += more_users

                del ids[:100]
        except tweepy.RateLimitError as e:
            # TODO - Don't just print error - we need solution to replay getting information 
            #        about users (i.e. lookup_users) from this point
            print "Rate limits on lookup_users was exeeded."
            print e
        ret[guy] = map(lambda x: { "id": x.id, "name": x.screen_name, "image_url": x.profile_image_url}, snd_followers)

    return JsonResponse(ret)

def get_followers_json(request, user_id):
    if not user_id:
        return JsonResponse({ 'message': 'You should provide user_id.' })

    frs_followers_ids = get_followers(user_id)
    if not frs_followers_ids:
        return JsonResponse({ 'message': 'Link has been expired.' })
    snd_followers_ids = []
    for uid in frs_followers_ids:
        snd_followers_ids += get_followers(uid)

    ret = defaultdict(int)
    for uid in snd_followers_ids:
        user = get_user(uid)
        if user:
            ret[user.screen_name] += 1

    return JsonResponse(ret)


from django.conf import settings

from django.core.cache import caches

import tweepy


ALL_DAY = 60 * 60 * 24
ALL_MONTH = ALL_DAY * 30
cache = caches['database']

class UserCompressed(object):
	def __init__(self, uid, screen_name, profile_image_url):
		self.id = uid
		self.screen_name = screen_name
		self.profile_image_url = profile_image_url

def set_friends(uid, friends):
	cache.set("fri_" + str(uid), friends, ALL_MONTH)

def get_friends(uid):
	return cache.get("fri_" + str(uid))

def set_followers(uid, followers):
	cache.set("fl_" + str(uid), followers, ALL_MONTH)

def get_followers(uid):
	return cache.get("fl_" + str(uid))

def set_user(uid, user):
	cache.set("u_" + str(uid), UserCompressed(user.id, user.screen_name, user.profile_image_url), ALL_MONTH)

def get_user(uid):
	return cache.get("u_" + str(uid))

class Context(object):
    def __init__(self, api, request, followers_ids_limit=5):
        self.api = api
        self.request = request
        self.limits = {
            'followers_ids': followers_ids_limit,
        }

def get_or_generate(ctx, uid):
    ret = get_followers(uid)
    if ret == None and ctx.limits['followers_ids']:
        try:
            ret = ctx.api.followers_ids(id=uid)
        except tweepy.RateLimitError:
            ret = None
        except tweepy.TweepError:
            ret = []

        if ret != None:
            set_followers(uid, ret)
        ctx.limits['followers_ids'] -= 1

    return ret or []
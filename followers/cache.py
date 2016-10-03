from django.conf import settings

from django.core.cache import caches


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
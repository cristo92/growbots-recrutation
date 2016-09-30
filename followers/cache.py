#from django.core.cache import caches
from django.core.cache import cache

ALL_DAY = 60 * 60 * 24
ALL_MONTH = ALL_DAY * 30
#cache = caches['database']

def set_friends(uid, friends):
	cache.set("__user__" + str(uid), friends, ALL_MONTH)

def get_friends(uid):
	return cache.get("__user__" + str(uid))
from django.core.cache import caches

ALL_DAY = 60 * 60 * 24
cache = caches['database']

def set_friends(uid, friends):
	cache.set("__user__" + str(uid), friends, ALL_DAY)

def get_friends(uid):
	return cache.get("__user__" + str(uid))
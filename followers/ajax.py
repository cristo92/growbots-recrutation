from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from functional import foldl
from cache import set_friends, get_friends

import tweepy

from views import authorize, Context, count_common_friends, get_or_generate

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
			else:
				print e
	return JsonResponse(ret)
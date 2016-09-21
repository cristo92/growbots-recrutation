from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import tweepy

def index(request):
	template = loader.get_template('followers/index.html')
	llist = [i for i in range(0, 10)]

	#get oauth from GET
	consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
	consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"
	access_token=request.GET.get('oauth_token', None)
	access_token_secret=request.GET.get('oauth_verifier', None)

	context = { 
		'basic_list': llist, 
		'name': None
	}

	if(access_token):

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.secure = True

		api = tweepy.API(auth)

		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)

		context['name'] = api.me().name

	return HttpResponse(template.render(context, request))

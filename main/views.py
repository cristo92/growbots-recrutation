from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import tweepy

def index(request):
	template = loader.get_template('main/index.html')

	consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
	consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.secure = True
	
	context = { "authorization_url": auth.get_authorization_url() }
	return HttpResponse(template.render(context, request))

def oauthorize():
	# == OAuth Authentication ==
	consumer_key="XnZcVbUhuLyR0rkgDaXXuNcBC"
	consumer_secret="yOk9R7xarlWN68S88xP1PqDnX3CGDPndw7gUPKNbIPLGgjNNji"

	access_token="778627306789240832-20ELlzX0OYcf41z4Pqinls6Pb3lw3ce"
	access_token_secret="AMF35NuEhltDdtmzbZGqOrkS74veJBpblajSwtDdXAjJu"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.secure = True
	print auth.get_authorization_url()


	"""auth.get_access_token("verifier_value")


	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	print(api.me().name)

	api.update_status(status='Updating using OAuth authentication via Tweepy!')
"""
# Introduction

I was using Django, jQuery and tweepy (full list of toolchain below). List of followers/followers is computed asynchronically in the background and send back
to browser by AJAX and stored in MemCachier (https://www.memcachier.com). Everything is deployed to Heroku 
(https://still-retreat-54855.herokuapp.com/). Non-trivial functions are well-documented in the source code. There are some TODOs
in the code - to mark down places which I'm aware they should be fixed - I didn't find it resonable to spend huge amount of time 
on focusing on every detail. JSON link for 'technical user' is generated from data from MemCachier (so it's session/cookie-free).

# File description

There are two main apps in this Django project:

  * main - app for showing main page. Very tiny and easy.
  * followers - app for showing /followers/followers, with AJAX, jQuery, cache, etc.
  
# Tweeter api limit problem

There are bunch of my solutions (with information if implemented):
 
 * cache (implemented) - cache twitter responses
 * asynchronous requests (implemented) - used for providing list of second followers. I use AJAX here. This feature is very
 important because sometimes we need more requests than we can use in 15min window for providing the list. With asynchronous 
 requests we can provide part of content for user while he or she waits for other part.
 * keep global information how much request left (not implemented) - I think it's very important to have this information,
 it is needed for next solutions
 * system of prioritize request (not implement) - when we have many users - we may want to prioritize getting content from twitter for ones,
 who are waiting for the first part of content (ones who have partial content can wait longer). As well as we may want to
 prioritize users who bought premium accounts in our service.
 * before rendering page create thread, which gets content from twitter. (not implement)
 
# Tools

  * Django
  * tweepy (https://github.com/tweepy/tweepy) - python library for twitter API
  * MemCachier (https://www.memcachier.com) - for providing cache
  
# URL

https://still-retreat-54855.herokuapp.com/

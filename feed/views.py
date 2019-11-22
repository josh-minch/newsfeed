import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from newsapi import NewsApiClient

from env import get_env_value
from .models import Article


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index(request):
    #newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    #top_headlines_response = newsapi.get_top_headlines(page_size=100)
    top_headlines_response = json.load(open('top_headlines_response.json'))
    if top_headlines_response['status'] == 'ok':
        articles = top_headlines_response['articles']

    for article in articles:
        article['urlToImage'] = 'fish.png'

    context = {'articles': articles}
    return render(request, 'feed/index.html', context)

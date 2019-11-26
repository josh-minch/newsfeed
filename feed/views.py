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
    print('index')
    #newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    #top_headlines_response = newsapi.get_top_headlines(page_size=100)
    top_headlines_response = json.load(open('top_headlines_response.json'))
    if top_headlines_response['status'] == 'ok':
        articles = top_headlines_response['articles']

    n_cols = 2
    rows = []
    for i in range(0, len(articles), n_cols):
        row = articles[i: i + n_cols]
        rows.append(row)

    context = {'articles': rows}
    return render(request, 'feed/index.html', context)

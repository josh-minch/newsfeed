from __future__ import absolute_import, unicode_literals
from celery import shared_task

from newsapi import NewsApiClient

from .models import Article
from env import get_env_value

import json

@shared_task
def refresh_articles():
    """ Refresh database with top 100 newest articles """
    # Clear current articles
    Article.objects.all().delete()

    n_articles = 100
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    top_headlines_response = newsapi.get_top_headlines(page_size=n_articles)
    #top_headlines_response = json.load(open('top_headlines_response.json'))

    if top_headlines_response['status'] == 'ok':
        articles = top_headlines_response['articles']

    for article in articles:
        article_data = extract_article_data(article)
        a = Article(**article_data)
        a.save()


def extract_article_data(article):
    source = article['source']['name']
    title = article['title']
    description = article['description']
    url = article['url']
    url_to_image = article['urlToImage']
    pub_date = article['publishedAt']

    return {'source': source, 'title': title, 'description': description,
            'url': url, 'url_to_image': url_to_image, 'pub_date': pub_date}

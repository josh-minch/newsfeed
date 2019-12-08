""" Automated celery tasks that use the NewsAPI to retrive top headline articles """
from __future__ import absolute_import, unicode_literals

from random import shuffle

from celery import shared_task
from newsapi import NewsApiClient

from env import get_env_value

from .models import Article

n_articles = 100
categories = ['business', 'entertainment', 'general',
                  'health', 'science', 'sports', 'technology']


@shared_task
def refresh_articles():
    """ Refresh database with newest articles, tagging each with their category """
    # First clear old db entries
    Article.objects.all().delete()

    # Get new articles, tagging each with their respective category
    articles = {}
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    for category in categories:
        response = newsapi.get_top_headlines(
            country='us', category=category, page_size=n_articles)

        if response['status'] != 'ok':
            continue
        articles = response['articles']

        for article in articles:
            article['category'] = category

    shuffle(articles)

    for article in articles:
        save_article(article)

def save_article(article):
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
    category = article['category']

    return {'source': source, 'title': title, 'description': description,
            'url': url, 'url_to_image': url_to_image, 'pub_date': pub_date,
            'category': category}

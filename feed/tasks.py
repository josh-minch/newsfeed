""" Automated celery tasks that use the NewsAPI to retrive top headline articles """
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from random import shuffle

from newsapi import NewsApiClient

from .models import Article
from env import get_env_value

import json

n_articles = 100
categories = ['business', 'entertainment', 'general',
                  'health', 'science', 'sports', 'technology']


def refresh_articles_long():
    Article.objects.all().delete()

    articles = []
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    for category in categories:
        response = newsapi.get_top_headlines(
            category=category, page_size=n_articles)

        if response['status'] == 'ok':
            articles = response['articles']
        else:
            continue

        for article in articles:
            article_data = extract_article_data(article)
            a = Article(**article_data)
            a.category = category
            a.save()


@shared_task
def refresh_articles():
    """ Refresh database with newest articles """
    Article.objects.all().delete()

    category_to_articles = get_articles()

    for category in categories:
        articles = category_to_articles[category]
        save_articles(articles, category)

def get_articles():
    """ Get articles in each cateogory """
    category_to_articles = dict()
    for category in categories:
        articles = request_articles_in_category(category)
        category_to_articles[category] = articles

    return category_to_articles

def request_articles_in_category(category):
    """ Get 100 top headline articles for specific news category """
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    response = newsapi.get_top_headlines(category=category, page_size=n_articles)

    if response['status'] == 'ok':
        articles = response['articles']

    return articles


def save_articles(articles, category):
    """ Save articles to database, including which category it belongs to """
    for article in articles:
        article_data = extract_article_data(article)
        a = Article(**article_data)
        a.category = category
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

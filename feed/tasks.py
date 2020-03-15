""" Automated celery tasks that use the NewsAPI to retrive top headline articles """
from __future__ import absolute_import, unicode_literals

from datetime import datetime
from random import shuffle

from celery import shared_task
from newsapi import NewsApiClient

from env import get_env_value

from .categories import categories
from .models import Article


n_articles = 100

@shared_task
def refresh_articles():
    """ Refresh database with newest articles, tagging each with their category """
    # Get datetime of last published article, so we know which articles are new and which
    # have already been saved to database. We replace the timezone data with None because
    # all articles are in UTC time, but the UTC flag type differs between Django and NewsAPI
    ordered_articles = Article.objects.all().order_by('-pub_date')
    if not ordered_articles:
        datetime_cutoff = datetime.today().replace(tzinfo=None)
    else:
        datetime_cutoff = ordered_articles[0].pub_date.replace(tzinfo=None)

    articles = []
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    for category in categories:
        response = newsapi.get_top_headlines(
            country='us', category=category, page_size=n_articles)

        if response['status'] != 'ok':
            continue
        all_response_articles = response['articles']

        # Filter out old articles to avoid saving duplicates to database
        new_articles = []
        for article in all_response_articles:
            article_datetime = get_article_datetime(article)

            if article_datetime > datetime_cutoff:
                article['category'] = category
                new_articles.append(article)

        articles += new_articles

    for article in articles:
        save_article(article)

def get_article_datetime(article):
    datetime_str = article['publishedAt']
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=None)

def request_articles(newsapi, category):
    response = newsapi.get_top_headlines(
        country='us', category=category, page_size=n_articles)

    if response['status'] != 'ok':
        return
    return response['articles']

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

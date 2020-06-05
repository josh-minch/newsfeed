""" Automated celery tasks that use the NewsAPI to retrive top headline articles """
from __future__ import absolute_import, unicode_literals

from datetime import datetime
from random import shuffle

from celery import shared_task
from django.utils import timezone
from newsapi import NewsApiClient

from env import get_env_value

from .categories import categories
from .models import Article

n_article_request = 100
article_db_limit = 7500

@shared_task
def refresh_articles():
    """ Refresh database with newest articles after a datetime cutoff,
    tagging each with their category. """
    datetime_cutoff = get_datetime_cutoff()

    articles = []
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    for category in categories:
        response = newsapi.get_top_headlines(
            n_country='us', category=category, page_size=n_article_request)

        if response['status'] != 'ok':
            print_error(response)
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


@shared_task
def delete_oldest_articles():
    """ Our free hosting plan limits our data storage to 10,000 records
    Therefore, we must periodically remove the oldest articles from our database
    to accomodate this limitation
    """
    articles = Article.objects.all().order_by('-pub_date')[article_db_limit:]

    for article in articles:
        article.delete()

def print_error(response):
    print(response['code'])
    print(response['message'])

def get_datetime_cutoff():
    """ Get datetime of last published article, so we know which articles are new and which
    have already been saved to database. """
    ordered_articles = Article.objects.all().order_by('-pub_date')

    # If database is empty, start cutoff to this morning
    if not ordered_articles:
        return datetime.today().replace(hour=0, minute=0, second=0, tzinfo=timezone.utc)
    else:
        return ordered_articles[0].pub_date.replace(tzinfo=timezone.utc)

def get_article_datetime(article):
    datetime_str = article['publishedAt']
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

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



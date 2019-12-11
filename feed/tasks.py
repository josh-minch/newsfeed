""" Automated celery tasks that use the NewsAPI to retrive top headline articles """
from __future__ import absolute_import, unicode_literals

from random import shuffle

from celery import shared_task
from newsapi import NewsApiClient

from env import get_env_value

from .models import Article
from .categories import categories

n_articles = 100

@shared_task
def refresh_articles():
    """ Refresh database with newest articles, tagging each with their category """
    # Get the id of the last element that was added to db.
    # This marks the end of the old articles that will later be deleted.
    max_id = Article.objects.last().id

    # Get new articles, tagging each with their respective category
    articles = []
    newsapi = NewsApiClient(get_env_value('NEWS_API_KEY'))
    for category in categories:
        response = newsapi.get_top_headlines(
            country='us', category=category, page_size=n_articles)

        if response['status'] != 'ok':
            continue
        category_articles = response['articles']

        for article in category_articles:
            article['category'] = category

        articles += category_articles

    shuffle(articles)
    for article in articles:
        save_article(article)

    # Delete old articles
    Article.objects.filter(id__lte=max_id).delete()

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

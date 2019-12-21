from random import shuffle

from django.shortcuts import render

from .models import Article
from .tasks import refresh_articles


def articles(request, category=''):
    if category == '':
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(category=category)

    rows = partition_articles(articles, 2)[:20]
    title = get_title(category)

    context = {'articles': rows, 'category': category, 'title': title}
    return render(request, 'feed/index.html', context)

def partition_articles(articles, n_cols):
    rows = []
    for i in range(0, len(articles), n_cols):
        row = articles[i: i + n_cols]
        rows.append(row)
    return rows

def login(request):
    context = {}
    return render(request, 'feed/login.html', context)

def get_title(category):
    if category == '':
        return 'All Feeds'
    return category.capitalize()

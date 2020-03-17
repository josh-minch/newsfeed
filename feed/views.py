from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (HttpResponse, HttpResponseRedirect, redirect,
                              render)
from django.views.decorators.cache import never_cache

from .models import Article
from .tasks import refresh_articles

@never_cache
def articles(request, category=''):
    if category == '':
        articles = Article.objects.all().order_by('-pub_date')
    else:
        articles = Article.objects.filter(
            category=category).order_by('-pub_date')

    if request.user.is_authenticated:
        set_if_favorite(request, articles)
    rows = partition_articles(articles, 2)

    paginator = Paginator(rows, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    wide_title, narrow_title = get_titles(category)
    context = {'category': category,
               'wide_title': wide_title,
               'narrow_title': narrow_title,
               'page_obj': page_obj}
    return render(request, 'feed/index.html', context)


@login_required
def favorite_article(request, article_id):
    article = Article.objects.filter(id=article_id).first()
    if request.user.favorites.filter(id=article_id).exists():
        request.user.favorites.remove(article)
        is_favorited = False
    else:
        request.user.favorites.add(article)
        is_favorited = True

    return HttpResponse(is_favorited)

def set_if_favorite(request, articles):
    for article in articles:
        if article in set(request.user.favorites.all()):
            article.favorited = True

def partition_articles(articles, n_cols):
    rows = []
    for i in range(0, len(articles), n_cols):
        row = articles[i: i + n_cols]
        rows.append(row)
    return rows

def get_titles(category):
    if category == '':
        return 'All Feeds', 'Newsfeed'
    return category.capitalize(), category.capitalize()

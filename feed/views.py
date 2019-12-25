from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

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


def favorite_article(request, article_id):
    if not request.user.is_authenticated:
        return redirect('users:register')

    article = Article.objects.filter(id=article_id).first()
    request.user.favorites.add(article)
    messages.success(request, f"Article {article_id} favorited")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def partition_articles(articles, n_cols):
    rows = []
    for i in range(0, len(articles), n_cols):
        row = articles[i: i + n_cols]
        rows.append(row)
    return rows

def get_title(category):
    if category == '':
        return 'All Feeds'
    return category.capitalize()

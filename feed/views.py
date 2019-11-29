from django.shortcuts import render

from .models import Article


def index(request):
    articles = Article.objects.all()

    n_cols = 2
    rows = partition_articles(articles, n_cols)

    context = {'articles': rows}
    return render(request, 'feed/index.html', context)


def partition_articles(articles, n_cols):
    rows = []
    for i in range(0, len(articles), n_cols):
        row = articles[i: i + n_cols]
        rows.append(row)
    return rows

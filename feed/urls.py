from django.urls import path, re_path

from . import views
from .categories import categories

app_name = 'feed'

category_re = r'^(?P<category>{})'.format('|'.join(categories))

urlpatterns = [
    path('', views.articles, name='all'),
    re_path(category_re, views.articles, name='category'),
    path('login/', views.login, name='login')
]

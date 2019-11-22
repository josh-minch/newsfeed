from django.urls import path

from . import views


app_name = 'feed'

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /feed/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /feed/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /feed/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

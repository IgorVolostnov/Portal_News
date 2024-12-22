from django.urls import path
from .views import NewsList, ArticlesList, PostDetail, NewsCreate, ArticlesCreate


urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail_news'),
   path('articles/<int:pk>', PostDetail.as_view(), name='post_detail_articles'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
]
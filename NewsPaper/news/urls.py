from django.urls import path
from .views import NewsList, ArticlesList, PostDetail, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, \
   NewsDelete, ArticlesDelete, upgrade_me, CategoryNewsList, Subscribers
from django.views.decorators.cache import cache_page


# Определяем все url-пути в приложении news
urlpatterns = [
   path('news/', cache_page(60*5)(NewsList.as_view()), name='news_list'),
   path('articles/', cache_page(60*5)(ArticlesList.as_view()), name='articles_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail_news'),
   path('articles/<int:pk>', PostDetail.as_view(), name='post_detail_articles'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('news/upgrade/', upgrade_me, name = 'upgrade'),
   path('categories/upgrade/', upgrade_me, name = 'upgrade'),
   path('categories/<int:value>', cache_page(60*5)(CategoryNewsList.as_view()), name='category_post_list'),
   path('subscribers/<int:value>', cache_page(60*5)(Subscribers.as_view()), name = 'subscribers'),
]
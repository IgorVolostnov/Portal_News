from django.urls import path, re_path
from .views import NewsList, ArticlesList, PostDetail, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, NewsDelete, ArticlesDelete, activate

urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail_news'),
   path('articles/<int:pk>', PostDetail.as_view(), name='post_detail_articles'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   re_path('activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
]
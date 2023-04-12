from django.urls import path, include
from .views import *

urlpatterns = [
    path('news', PostList.as_view(), name='news'),
    path('author/', AuthorList.as_view()),
    path('<int:pk>', DetailPost.as_view(), name='detail'),
    path('news/search/', SearchList.as_view(model=Post), name='search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('accounts/', include('django.contrib.auth.urls'))
]

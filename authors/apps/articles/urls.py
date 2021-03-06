from django.urls import path, include

from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/ratings/', include('authors.apps.rating.urls',
                                             namespace='ratings')),
    path('articles/<slug>/like/',
         views.LikeArticleApiView.as_view(), name='likes'),
    path('articles/<slug>/dislike/',
         views.DislikeArticleApiView.as_view(), name='dislikes'),
    path('tags/', views.TagsAPIView.as_view(), name="articles-tags")
]

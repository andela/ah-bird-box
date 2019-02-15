from django.urls import path, include

from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/ratings/', include('authors.apps.rating.urls',
                                             namespace='ratings'))
]

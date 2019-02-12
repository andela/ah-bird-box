from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details')
]

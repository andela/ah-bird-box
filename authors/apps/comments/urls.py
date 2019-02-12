from django.urls import path, include

from .views import CommentsAPIView, CommentDetailsAPIView

app_name = 'comments'
urlpatterns = [
    path('articles/<slug>/comments/', CommentsAPIView.as_view(),
         name='comments'
         ),
    path('api/', include(('authors.apps.articles.urls',
                          'articles'), namespace='articles')),
    path('articles/<slug>/comments/<int:id>/',
         CommentDetailsAPIView.as_view(),
         name='specific_comment'
         ),
]

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView,
    ListAPIView)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from .permissions import IsOwnerOrReadonly
from .renderers import ArticleJsonRenderer
from .serializers import ArticleSerializers, TagsSerializer
from .models import Article, Tag


def article_not_found():
    raise ValidationError(
        detail={'error': 'No article found for the slug given'})


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListCreateArticle(ListCreateAPIView):
    pagination_class = StandardPagination
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        article = request.data
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        article_instance = serializer.save(author=request.user)
        if article_instance.image_url is not None:
            article_instance.image_url = article_instance.image_url.url
            article_instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = ArticleSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RetrieveUpdateDeleteArticle(RetrieveUpdateDestroyAPIView):
    """
    This class retrieves, updates, and deletes a single article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    renderer_classes = (ArticleJsonRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    lookup_field = 'slug'

    def get_single_article(self, slug):
        """
        This method returns an article specified by a slug
        """
        article = Article.objects.filter(slug=slug).first()
        return article

    def get(self, request, slug):
        article = self.get_single_article(slug)
        if not article:
            article_not_found()
        return super().get(request, slug)

    def update(self, request, slug):
        """
        This method updates an article
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            article_not_found()

        article_data = request.data
        serializer = self.serializer_class(
            article, data=article_data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, article)
            article_instance = serializer.save()
            if article_instance.image_url is not None:
                article_instance.image_url = article_instance.image_url.url
                article_instance.save()
            return Response(serializer.data)

    def delete(self, request, slug):
        if not self.get_single_article(slug):
            article_not_found()
        super().delete(self, request, slug)
        return Response({"message": "Article Deleted Successfully"})


class LikeArticleApiView(UpdateAPIView):
    """Like an article."""
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializers

    def put(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        if article in Article.objects.filter(
                disliked_by=request.user):
            article.disliked_by.remove(request.user)

        if article in Article.objects.filter(
                liked_by=request.user):
            article.liked_by.remove(request.user)

        else:
            article.liked_by.add(request.user)

        serializer = self.serializer_class(article,
                                           context={'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class DislikeArticleApiView(UpdateAPIView):
    """Dislike an Article."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializers

    def put(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        if article in Article.objects.filter(
                liked_by=request.user):
            article.liked_by.remove(request.user)

        if article in Article.objects.filter(
                disliked_by=request.user):
            article.disliked_by.remove(request.user)

        else:
            article.disliked_by.add(request.user)

        serializer = self.serializer_class(article,
                                           context={'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TagsAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response({'tags': serializer.data}, status=status.HTTP_200_OK)

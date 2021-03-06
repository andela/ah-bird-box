from rest_framework.generics import (RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authors.apps.articles.models import Article
from .models import Comments
from .serializers import CommentsSerializers, CommentsHistorySerializers


class CommentsAPIView(APIView):
    """
    Creates a CRUD view for all comments
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentsSerializers

    def get(self, request, **kwargs):
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "error": "Sorry, article was not found"
                    }
                },
                status=status.HTTP_200_OK
            )

        queryset = Comments.objects.filter(article=article.id)
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid()
        return Response({
            "comment": serializer.data,
            "commentsCount": queryset.count()
        },
            status=status.HTTP_200_OK
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """
        Method for creating comments
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response(
                {
                    "comment": {
                        "error": "Sorry, article was not found"
                    }
                },
                status=status.HTTP_204_NO_CONTENT
            )
        comment = request.data
        serializer = self.serializer_class(data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailsAPIView(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    """
    Creates a view to Get, update, and delete a particular comment
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentsSerializers

    def get(self, request, id, **kwargs):
        """
        Get a particular comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "error": "Sorry, article was not found"
                    }
                },
                status=status.HTTP_200_OK
            )
        queryset = Comments.objects.filter(id=id, article=article.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            "comment": serializer.data,
            "commentsCount": queryset.count()
        },
            status=status.HTTP_200_OK
        )

    def create(self, request, slug, id):
        """Method for creating a child comment on parent comment."""

        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
        try:
            parent_comment = article.comments.filter(id=id).first().pk
        except AttributeError:
            message = {
                "Error": "Sorry, comment was not found"
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        body = request.data['body']

        data = {
            'body': body,
            'parent': parent_comment,
            'article': article.pk,
            'author': request.user.id
        }

        serializer = self.serializer_class(
            data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id, **kwargs):
        """
        Delete a particular comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, article was not found"
                    }
                },
                status=status.HTTP_204_NO_CONTENT
            )
        queryset = Comments.objects.filter(id=id, article=article.id)
        comment = Comments.objects.filter(id=id, article=article.id).first()
        if not queryset:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, comment was not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user.pk != comment.author.id:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, you are not authorized to delete this comment"  # noqa
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        queryset[0].delete()
        return Response(
            {
                "comment": {
                    "message": "Comment was successfully deleted"
                }
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, id, **kwargs):
        """
        Update a particular comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, article was not found"
                    }
                },
                status=status.HTTP_204_NO_CONTENT
            )
        comment = Comments.objects.filter(id=id, article=article.id).first()
        if not comment:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, comment was not found"
                    }
                },
                status=status.HTTP_204_NO_CONTENT
            )

        if request.user.pk != comment.author.id:
            return Response(
                {
                    "comment": {
                        "message": "Sorry, you are not authorized to update this comment"  # noqa
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment_data = request.data
        serializer = self.serializer_class(
            comment, data=comment_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Comment was successfully updated",
                "comment": serializer.data
            },
                status=status.HTTP_200_OK
            )


class CommentsHistoryAPIView(ListCreateAPIView):
    """
    Creates a view to retrieve the edit history of comments
    """
    serializer_class = CommentsHistorySerializers
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, **kwargs):

        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response(
                {
                    "error": "Sorry, article was not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        comments = Comments.objects.filter(id=id, article=article.id).first()
        if not comments:
            return Response(
                {
                    "error": "Sorry, comment was not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        id = self.kwargs['id']
        edited_comment = Comments.history.filter(id=id)
        if edited_comment.count() == 1:
            return Response(
                {
                    'error': 'No edit history for this comment found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(edited_comment, many=True)
        data = {
            'Comment Edit History': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

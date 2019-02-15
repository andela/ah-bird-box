from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.articles.models import Article
from authors.apps.rating.renderers import RatingsRenderer
from authors.apps.rating.serializers import RatingsSerializer


class RatingsRetrieveAPIView(ListCreateAPIView):
    """
    This class get's the user's profile from the database according to the
    username given in the URL
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (RatingsRenderer,)
    serializer_class = RatingsSerializer
    queryset = Article.objects.all()

    @staticmethod
    def get_article(slug: str):
        return Article.objects.get(slug=slug)

    def get_serializer_context(self):
        """
        Add the article to the serialier context
        :return: context
        """
        context = super().get_serializer_context()
        try:
            context['article'] = self.get_article(
                slug=self.request.parser_context['kwargs']['slug'])
        except Article.DoesNotExist:
            context['article'] = None
        return context

    def list(self, request, *args, **kwargs):
        """
        Overrides the default method so as to return the ratings alone.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # get the article from the database and set its ratings as the queryset
        # this will be used in the serializer, return error if not found
        try:
            article = self.get_article(kwargs['slug'])
            self.queryset = article.ratings.all()
            return super().list(request, *args, **kwargs)
        except Article.DoesNotExist:
            output = dict(errors='Article not found')
            return Response(output, 404)

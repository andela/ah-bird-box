from django.db import models
from authors.apps.authentication.models import User
from authors.apps.core.models import TimestampMixin
from authors.apps.articles.models import Article


class Comments(TimestampMixin, models.Model):
    """
    Creates model for Comments
    """

    body = models.TextField(blank=False, max_length=200)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments', null=True)
    is_deleted = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='threads',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.body

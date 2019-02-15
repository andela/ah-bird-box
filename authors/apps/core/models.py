from django.db import models


class TimestampMixin(models.Model):
    """
    Creates created_at and updated_at fields
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """
        Creates created_at and updated_at fields to other models which
        inherits this model class
        """
        abstract = True
        ordering = ['-created_at', '-updated_at', '-id']

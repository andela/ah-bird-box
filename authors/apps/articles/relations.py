import re

from django.utils.text import slugify
from rest_framework import serializers

from authors.apps.articles.models import Tag


class TagsRelation(serializers.RelatedField):
    """
    Class that overwrites the serializer class for tags
    to enable tags are saved on a separate table upon
    article creation
    """

    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):
        return value.tag

    def to_internal_value(self, data):
        """
        Method to ensure tags with spaces and caps are saved
        as slugs, and tags with uppercase and lowercase are
        saved as one as well as ensure tags have no special characters
        """
        if not re.match(r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$', data):
            raise serializers.ValidationError(
                'Tag cannot have special characters')
        new_tag = slugify(data)
        tag, created = Tag.objects.get_or_create(tag=new_tag)
        return tag

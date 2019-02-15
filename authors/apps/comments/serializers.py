from rest_framework import serializers
from .models import Comments


class CommentsSerializers(serializers.ModelSerializer):
    """
    Creates a serializer for the Comments model
    """
    author = serializers.SerializerMethodField()
    article_id = serializers.SerializerMethodField()
    body = serializers.CharField(
        required=True,
        max_length=200,
        error_messages={
            'required': 'The comment body cannot be empty',
        }
    )

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def to_representation(self, instance):
        """
        overide representation for custom output
        """
        threads = [
            {

                'id': thread.id,
                'body': thread.body,
                'author': thread.author.id,
                'created_at': self.format_date(thread.created_at),
                'replies': thread.threads.count(),
                'updated_at': self.format_date(thread.updated_at)
            } for thread in instance.threads.all()
        ]

        representation = super(CommentsSerializers,
                               self).to_representation(instance)
        representation['created_at'] = self.format_date(instance.created_at)
        representation['updated_at'] = self.format_date(instance.updated_at)
        representation['author'] = instance.author.id
        representation['article'] = instance.article.title
        representation['reply_count'] = instance.threads.count()
        representation['threads'] = threads
        del representation['parent']

        return representation

    class Meta:
        model = Comments
        fields = ('id', 'created_at', 'updated_at', 'body', 'author',
                  'article_id', 'parent')

        read_only_fields = ('id',
                            'created_at', 'updated_at', 'article_id')

    def get_author(self, obj):
        return obj.author.id

    def get_article_id(self, obj):
        return obj.article.id

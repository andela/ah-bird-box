from rest_framework import serializers

from .models import Article, Tag
from authors.apps.articles.relations import TagsRelation


class ArticleSerializers(serializers.ModelSerializer):
    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def to_representation(self, instance):
        representation = super(ArticleSerializers,
                               self).to_representation(instance)
        representation['created_at'] = self.format_date(instance.created_at)
        representation['updated_at'] = self.format_date(instance.updated_at)
        return representation

    title = serializers.CharField(
        required=True,
        max_length=140,
        error_messages={
            'required': 'Title is required',
            'max_length': 'Title cannot be more than 140'
        }
    )
    description = serializers.CharField(
        required=False,
        max_length=250,
        error_messages={
            'max_length': 'Description cannot be more than 250'
        }
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Body cannot be empty'
        }
    )

    author = serializers.SerializerMethodField(read_only=True)

    slug = serializers.CharField(read_only=True)

    averageRating = serializers.SerializerMethodField()
    ratingsCount = serializers.SerializerMethodField()
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    disliked_by = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    tags = TagsRelation(many=True, required=False)

    @staticmethod
    def get_averageRating(article):
        """
        Calculates weighted average rating.
        :param article: The article whose ratings we are calculating
        :return: None if no one has rated, The weighted average to 2 decimal
        places
        :rtype: float or None
        """
        all_ratings = article.ratings.all().count()
        fives = article.ratings.filter(stars=5).count()
        fours = article.ratings.filter(stars=4).count()
        threes = article.ratings.filter(stars=3).count()
        twos = article.ratings.filter(stars=2).count()
        ones = article.ratings.filter(stars=1).count()

        if all_ratings < 1:
            return None
        else:
            weighted_total = (5 * fives) + (4 * fours) + (3 * threes) + (
                2 * twos) + (1 * ones)
            weighted_average = weighted_total / all_ratings
            return round(weighted_average, 2)

    @staticmethod
    def get_ratingsCount(article):
        """
        Method for getting the number of people who have rated.
        :param article: The article to be rated
        :return:
        :rtype: int
        """
        return article.ratings.all().count()

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        model = Article
        fields = (
            'title',
            'description',
            'body',
            'slug',
            'image_url',
            'author',
            'tags',
            'created_at',
            'updated_at',
            'averageRating',
            'ratingsCount',
            'liked_by',
            'disliked_by',
            'likes_count',
            'dislikes_count'
        )

    def get_likes_count(self, obj):
        """"Total Likes"""
        return obj.liked_by.count()

    def get_dislikes_count(self, obj):
        """Total Dislikes"""
        return obj.disliked_by.count()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag')

    def to_representation(self, instance):
        return instance.tag

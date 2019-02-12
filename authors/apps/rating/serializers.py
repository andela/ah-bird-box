from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Rating


class RatingsSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects to return
    their profile alone"""
    user = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ('user', 'stars')

    @staticmethod
    def get_user(instance):
        # show the user's username only alongside the rating
        return instance.user.username

    def create(self, validated_data):
        """
        When the URL is accessed with the POST method this function is hit.
        :param validated_data:
        :return:
        """
        # set the article given from the context. It was set in our view
        article = self.context['article']

        # If the article is not found then raise error
        if article is None:
            raise ValidationError('Article not found')

        # get the current user from the context
        current_user = self.context['request'].user

        # if the article's author is the current user, raise error
        if article.author == current_user:
            raise ValidationError('You cannot rate your own article')

        # if the stars given are less than 1 or more than 5, raise error
        stars = validated_data['stars']
        if stars > 5 or stars < 1:
            raise ValidationError('Star ratings should be from 1 and 5 stars')

        # get the article's rating where the user is the current user
        rating = article.ratings.filter(user=current_user).first()

        # if it is found, then just update the stars
        if rating:
            rating.stars = stars
            rating.save()
        else:
            # if not found then create the rating in the Ratings table
            article.ratings.create(user=current_user, stars=stars)

        # return that rating to be displayed to the user
        return article.ratings.get(user=current_user, stars=stars)
